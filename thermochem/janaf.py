# janaf.py

# This module gets thermodynamic datat from the JANAF database.
# Files are downloaded from the NIST servers as needed and then cached locally.
#
# Zack Gainsforth
#
# Funding by NASA

from __future__ import division
from __future__ import print_function

import numpy as np
import pandas as pd
import os
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

class Janafdb(object):

    """
    Class that reads the NIST JANAF tables for thermodynamic data.

    Data is initially read from the web servers, and then cached.

    # >>> db = Elementdb()
    # >>> TiO = db.getelementdata("TiO", 'c,l')
    # >>> print(TiO)
    # <element> O2 REF ELEMENT
    # >>> print('molar mass',oxygen.mm)
    # molar mass 0.0319988
    # >>> print('heat capacity',oxygen.cp)
    # heat capacity 918.078952423
    #
    # The reference temperature for enthalpy is 298.15 K
    #
    # >>> print('enthropy',oxygen.so(298))
    # enthropy 205.133745795
    # >>> print('gibbs free energy',oxygen.go(298))
    # gibbs free energy -61134.2629008
    #
    # There's a search function.  It is very useful because some names
    # are a bit tricky.  Well, not this one.
    #
    # >>> db.search("AIR")
    # ['AIR']
    # >>> air = db.getelementdata("AIR")
    # >>> print('air molar mass',air.mm)
    # air molar mass 0.02896518
    # >>> print('heat capacity',air.cp)
    # heat capacity 1004.77625096
    # >>> print(round(air.density(101325,298), 6))
    # 1.184519
    #
    # The element database can create also mixtures.  It returns an
    # instance of Mixture object that can give you the same as the
    # Element class for any mixture.
    #
    # >>> mix = db.getmixturedata([("O2 REF ELEMENT",20.9476),\
    # ("N2  REF ELEMENT",78.084),\
    # ("CO2",0.0319),\
    # ("AR REF ELEMENT",0.9365),\
    # ])
    # >>> print(mix)
    # <Mixture>:
    #     O2 REF ELEMENT at 20.9476
    #     N2  REF ELEMENT at 78.084
    #     CO2 at 0.0319
    #     AR REF ELEMENT at 0.9365
    # >>> print(mix.cp)
    # 1004.72217065
    # >>> print(round(mix.mm, 6))
    # 0.028965
    """

    def __init__(self):
        """
        We have an index file which can be used to build the url for all phases on the NIST site.
        """

        # Read the index file which tells us the filenames for all the phases in the JANAF database.
        self.db = pd.read_csv("thermochem/JANAF_index.txt", delimiter='|')
        # Name the columns and trim whitespace off the text fields.
        self.db.columns = ['formula', 'name', 'phase', 'filename']
        self.db["formula"] = self.db["formula"].map(str.strip)
        self.db["name"] = self.db["name"].map(str.strip)
        self.db["phase"] = self.db["phase"].map(str.strip)
        self.db["filename"] = self.db["filename"].map(str.strip)

        # Make sure that the directory for cached JANAF files exists.
        self.JANAF_cachedir = os.path.join('.', 'thermochem', 'JANAF_Cache')
        if not os.path.exists(self.JANAF_cachedir):
            os.mkdir(self.JANAF_cachedir)

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

    def getphasedata(self, formula=None, name=None, phase=None, nocache=False):
        """
        Returns an element instance given the name of the element.
        formula, name and phase match the respective fields in the JANAF index.
        nocache = True means that we will always get the data from the web.

        >>> db = Janafdb()
        >>> db.getphasedata(formula='O2Ti', phase='cr')
        Traceback (most recent call last):
            ...
        ValueError: There are 2 records matching this pattern.
        >>> db.getphasedata(formula='Oxyz')
        Traceback (most recent call last):
            ...
        ValueError: Valid phase types are 'cr', 'l', 'cr,l', 'g', 'ref'.
        >>> db.getphasedata(formula='Oxyz', phase='l')
        Traceback (most recent call last):
            ...
        ValueError: Did not find Oxyz, None, (l)

        """

        # Check that the phase type requested is valid.
        if phase not in ['cr', 'l', 'cr,l', 'g', 'ref']:
            raise ValueError("Valid phase types are 'cr', 'l', 'cr,l', 'g', 'ref'.")

        # We can search on either an exact formula, partial text match in the name, and exact phase type.
        formulasearch = pd.Series(np.ones(len(self.db)), dtype=bool)
        namesearch = formulasearch.copy()
        phasesearch = formulasearch.copy()
        if formula is not None:
            formulasearch = self.db['formula'] == formula
        if name is not None:
            namesearch = self.db['name'].str.contains(name)
        if phase is not None:
            phasesearch = self.db['phase'] == phase
        searchmatch = formulasearch & namesearch & phasesearch

        # Get the record (should be one record) which specifies this phase.
        PhaseRecord = self.db[searchmatch]
        if len(PhaseRecord) == 0:
            raise ValueError("Did not find %s, %s, (%s)" % (formula, name, phase))
        if len(PhaseRecord) > 1:
            raise ValueError("There are %d records matching this pattern."%len(PhaseRecord))

        # At this point we have one record.  Check if we have that file cached.
        cachedfilename = os.path.join(self.JANAF_cachedir, PhaseRecord['filename'].values[0]+'.txt')
        if os.path.exists(cachedfilename) and nocache==False:
            # Yes it was cached, so let's read it into memory.
            with open(cachedfilename, 'r') as f:
                textdata = f.read()
        else:
            # No it was not cached so let's get it from the web.
            response = urllib2.urlopen('http://kinetics.nist.gov/janaf/html/%s.txt'%PhaseRecord['filename'].values[0])
            textdata = response.read()

            # And cache the data so we aren't making unnecessary trips to the web.
            if nocache==False:
                with open(cachedfilename, 'w') as f:
                    f.write(textdata)

        # And read the text file into a DataFrame.
        data = pd.read_csv(StringIO(textdata), skiprows=1, delimiter='\t*', header=0, engine='python')

        # TODO At this point, we should create a phase class.

        return data

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


if __name__ == '__main__':
    db = Janafdb()

    s = db.search('Ti')
    print(len(s))

    print(db.getphasedata(formula='O2Ti', name='Rutile', phase='cr', nocache=True))

    # mix = db.getmixturedata([("O2 REF ELEMENT", 20.9476),
    #                          ("N2  REF ELEMENT", 78.084),
    #                          ("CO2", 0.0319),
    #                          ("AR REF ELEMENT", 0.9365),
    #                          ("O2 REF ELEMENT", 1.2)])
    # mix.aggregate()

    # Test TiO phase

    # print(db.getelementdata('NiO  Solid-A'))
    # print(db.getelementdata('NiO  Solid-C'))
    # print(db.search('NiO'))
