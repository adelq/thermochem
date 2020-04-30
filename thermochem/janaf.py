"""
This module gets thermodynamic data from the JANAF database.
Files are downloaded from the NIST servers as needed and then cached locally.

Zack Gainsforth

Funding by NASA
"""

from __future__ import division
from __future__ import print_function

import os
import sys
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

try:
    # Python 3
    import urllib.request as urllib2
except ImportError:
    # Python 2
    import urllib2

try:
    # Python 2
    from StringIO import StringIO
except ImportError:
    # Python 3
    from io import StringIO

# Universal gas constant R
R = 8.314472
# Reference temp
Tr = 298.15 # K


class JanafPhase(object):
    """
    Class which is created by Janafdb for a specific phase.

    It reads in the JANAF data file and produces functions which interpolate
    the thermodynamic constants.

    Tr stands for reference temperature and is 298.15 K

    >>> db = Janafdb()
    >>> p = db.getphasedata(formula='O2Ti', name='Rutile', phase='cr')
    >>> p.cp([500, 550, 1800]).astype(int).tolist()
    [67, 68, 78]
    >>> print(p.S([500, 550, 1800]))        # Entropy in J/mol/K
    [  82.201    88.4565  176.876 ]
    >>> print(p.gef([500, 550, 1800]))      # [G-H(Tr)]/T in J/mol/K
    [  57.077   59.704  115.753]
    >>> print(p.hef([500, 550, 1800]))      # H-H(Tr) in kJ/mol
    [  12.562    15.9955  110.022 ]
    >>> print(p.DeltaH([500, 550, 1800]))   # Gibbs free energy in kJ/mol
    [-943670.  -943229.5 -936679. ]
    >>> print(p.DeltaG([500, 550, 1800]))   # Helmholtz free enegy in kJ/mol
    [-852157.  -843046.5 -621013. ]
    >>> p.logKf([500, 550, 1800]).astype(int).tolist() # Equilibrium constant of formation.
    [89, 80, 18]
    >>> print(p.cp(1000))                   # Heat capacity in J/mol/K
    74.852
    >>> print(p.cp(50000))                  # Example of erroneous extrapolation.
    Traceback (most recent call last):
        ...
    ValueError: A value in x_new is above the interpolation range.
    """

    def __init__(self, rawdata_text):
        # Store the raw data text file from NIST.
        self.rawdata_text = rawdata_text

        self.description = self.rawdata_text.splitlines()[0]

        # Read the text file into a DataFrame.
        data = pd.read_csv(
            StringIO(self.rawdata_text),
            skiprows=2,
            header=None,
            delimiter=r'[\t\s]+',
            engine='python',
            names=['T', 'Cp', 'S', '[G-H(Tr)]/T', 'H-H(Tr)', 'Delta_fH', 'Delta_fG', 'log(Kf)']
        )
        self.rawdata = data

        # Sometimes the JANAF files have funky stuff written in them.
        # (Old school text format...)
        # Clean it up.
        for c in data.columns:
            # We only need to polish up columns that aren't floating point
            # numbers.
            if np.issubdtype(data.dtypes[c], np.floating):
                continue
            # Change INFINITE to inf
            data.loc[data[c] == 'INFINITE', c] = np.inf
            # Anything else becomes a nan.
            # Convert to floats.
            data[c] = pd.to_numeric(data[c], errors='coerce')

        # Convert all units to Joules.
        data['Delta_fH'] *= 1000
        data['Delta_fG'] *= 1000

        # Handle NaNs for the phase transition points. This only affects
        # Delta_fG, Delta_fH, and log(Kf)
        good_indices = np.where(np.isfinite(data['Delta_fH']))

        # Now make interpolatable functions for each of these.
        self.cp = interp1d(self.rawdata['T'], self.rawdata['Cp'])
        self.S = interp1d(self.rawdata['T'], self.rawdata['S'])
        self.gef = interp1d(self.rawdata['T'], self.rawdata['[G-H(Tr)]/T'])
        self.hef = interp1d(self.rawdata['T'], self.rawdata['H-H(Tr)'])
        self.DeltaH = interp1d(self.rawdata['T'].iloc[good_indices],
                               self.rawdata['Delta_fH'].iloc[good_indices])
        self.DeltaG = interp1d(self.rawdata['T'].iloc[good_indices],
                               self.rawdata['Delta_fG'].iloc[good_indices])
        self.logKf = interp1d(self.rawdata['T'].iloc[good_indices],
                              self.rawdata['log(Kf)'].iloc[good_indices])

    def __str__(self):
        rep = super(JanafPhase, self).__str__()
        rep += "\n  "
        rep += self.description
        rep += "\n    Cp(%0.2f) = %0.3f J/mol/K" % (Tr, self.cp(Tr))
        rep += "\n    S(%0.2f) = %0.3f J/mol/K" % (Tr, self.S(Tr))
        rep += "\n    [G-H(%0.2f)]/%0.2f = %0.3f J/mol/K" % (Tr, Tr, self.gef(Tr))
        rep += "\n    H-H(%0.2f) = %0.3f J/mol/K" % (Tr, self.hef(Tr))
        rep += "\n    Delta_fH(%0.2f) = %0.0f J/mol" % (Tr, self.DeltaH(Tr))
        rep += "\n    Delta_fG(%0.2f) = %0.0f J/mol" % (Tr, self.DeltaG(Tr))
        rep += "\n    log(Kf((%0.2f)) = %0.3f" % (Tr, self.logKf(Tr))
        return rep


class Janafdb(object):
    """
    Class that reads the NIST JANAF tables for thermodynamic data.

    Data is initially read from the web servers, and then cached.

    Try:
        Rutile = Janafdb().getphasedata(name='Rutile')
        to load thermodynamic constants for TiO2, rutile.
    """
    VALIDPHASETYPES = ['cr', 'l', 'cr,l', 'g', 'ref', 'cd', 'fl', 'am', 'vit',
                       'mon', 'pol', 'sln', 'aq', 'sat']
    JANAF_URL = "https://janaf.nist.gov/tables/%s.txt"

    def __init__(self):
        """
        We have an index file which can be used to build the url for all phases
        on the NIST site.
        """

        # Read the index file which tells us the filenames for all the phases
        # in the JANAF database.
        dirname = os.path.dirname(__file__)
        janaf_index = os.path.join(dirname, 'JANAF_index.txt')
        self.db = pd.read_csv(janaf_index, delimiter='|')
        # Name the columns and trim whitespace off the text fields.
        self.db.columns = ['formula', 'name', 'phase', 'filename']
        self.db["formula"] = self.db["formula"].map(str.strip)
        self.db["name"] = self.db["name"].map(str.strip)
        self.db["phase"] = self.db["phase"].map(str.strip)
        self.db["filename"] = self.db["filename"].map(str.strip)

        # Make sure that the directory for cached JANAF files exists.
        self.JANAF_cachedir = os.path.join(dirname, 'JANAF_Cache')
        if not os.path.exists(self.JANAF_cachedir):
            os.mkdir(self.JANAF_cachedir)

    def __str__(self):
        rep = super().__str__()
        # rep = "\tFormula = %s"%self.db["formula"]
        rep += "\n  Try:\n"
        rep += "    Janafdb().search('Ti')\n"
        rep += "  or:\n"
        rep += "    Janafdb().getphasedata(name='Magnesium Oxide', phase='l')\n"
        return rep

    def search(self, searchstr):
        """
        List all the species containing a string. Helpful for
        interactive use of the database.
        returns a pandas dataframe containing valid phases.

        >>> db = Janafdb()
        >>> s = db.search('Rb-')
        >>> print(s)
             formula           name phase filename
        1710     Rb-  Rubidium, Ion     g   Rb-007
        >>> s = db.search('Ti')
        >>> print(len(s))
        88
        """

        formulasearch = self.db['formula'].str.contains(searchstr)
        namesearch = self.db['name'].str.contains(searchstr)

        return self.db[formulasearch | namesearch]

    def getphasedata(self, formula=None, name=None, phase=None, filename=None, cache=True):
        """
        Returns an element instance given the name of the element.
        formula, name and phase match the respective fields in the JANAF index.
        cache = False means that we will always get the data from the web.

        >>> db = Janafdb()
        >>> db.getphasedata(formula='O2Ti', phase='cr')
        Traceback (most recent call last):
            ...
        ValueError: There are 2 records matching this pattern:
            ...
        Please select a unique record.
        >>> db.getphasedata(formula='Oxyz')
        Traceback (most recent call last):
            ...
        ValueError: Did not find a phase with formula = Oxyz
                    Please provide enough information to select a unique record.
        >>> db.getphasedata(formula='Oxyz', phase='l')
        Traceback (most recent call last):
            ...
        ValueError: Did not find a phase with formula = Oxyz, phase = l
                    Please provide enough information to select a unique record.
        >>> FeO = db.getphasedata(formula='FeO', phase='cr,l')
        >>> print(FeO)
        <thermochem.janaf.JanafPhase object at 0x...>
          Iron Oxide (FeO)  Fe1O1(cr,l)
            Cp(298.15) = 49.915 J/mol/K
            S(298.15) = 60.752 J/mol/K
            [G-H(298.15)]/298.15 = 60.752 J/mol/K
            H-H(298.15) = 0.000 J/mol/K
            Delta_fH(298.15) = -272044 J/mol
            Delta_fG(298.15) = -251429 J/mol
            log(Kf((298.15)) = 44.049
        """

        # Check that the phase type requested is valid.
        if phase is not None:
            phase = phase.lower()
        if phase is not None and phase not in self.VALIDPHASETYPES:
            raise ValueError("Valid phase types are %s." % self.VALIDPHASETYPES)

        # We can search on either an exact formula, partial text match in the
        # name, and exact phase type.
        # Start with all records selected in the search, and then we trim.
        formulasearch = pd.Series(np.ones(len(self.db)), dtype=bool)
        namesearch = formulasearch.copy()
        phasesearch = formulasearch.copy()
        filenamesearch = formulasearch.copy()
        if formula is not None:
            # Select only records that match the chemical formula.
            formulasearch = self.db['formula'] == formula
        if name is not None:
            # Select records that match the chemical/mineral name.
            namesearch = self.db['name'].str.lower().str.contains(name.lower())
        if phase is not None:
            phasesearch = self.db['phase'] == phase
        if filename is not None:
            # Select only records that match the filename on the website (this is very unique.)
            filenamesearch = self.db['filename'].str.lower() == filename.lower()
        # Combine.
        searchmatch = formulasearch & namesearch & phasesearch & filenamesearch

        # Get the record (should be one record) which specifies this phase.
        phase_record = self.db[searchmatch]
        if phase_record.empty:
            searched = []
            if formula is not None:
                searched.append("formula = %s" % formula)
            if phase is not None:
                searched.append("phase = %s" % phase)
            if filename is not None:
                searched.append("filename = %s" % filename)
            search_string = ", ".join(searched)
            raise ValueError("""Did not find a phase with %s
            Please provide enough information to select a unique record.""" % (search_string))
        if len(phase_record) > 1:
            # The user has entered in data that does not uniquely select one
            # record. Let's help him out by listing his options unless it is
            # too many.
            raise ValueError("""There are %d records matching this pattern:
            %s

            Please select a unique record.""" % (len(phase_record), phase_record))

        # At this point we have one record.  Check if we have that file cached.
        cachedfilename = os.path.join(
            self.JANAF_cachedir,
            "%s.txt" % phase_record['filename'].values[0]
        )
        if cache and os.path.exists(cachedfilename):
            # Yes it was cached, so let's read it into memory.
            with open(cachedfilename, 'r') as f:
                textdata = f.read()
        else:
            # No it was not cached so let's get it from the web.
            response = urllib2.urlopen(Janafdb.JANAF_URL %
                                       phase_record['filename'].values[0])
            textdata = response.read()
            if sys.version_info[0] > 2:
                textdata = textdata.decode()

            # And cache the data so we aren't making unnecessary trips to the
            # web.
            if cache:
                with open(cachedfilename, 'w') as f:
                    f.write(textdata)

        # Create a phase class and return it.
        return JanafPhase(textdata)

    # def getmixturedata(self, components):
    #     """
    #     Creates a mixture of components given a list of tuples
    #     containing the formula and the volume percent
    #     """
    #     mixture = Mixture()
    #     for comp in components:
    #         mixture.add(self.getelementdata(comp[0]), comp[1])
    #
    #     return mixture
