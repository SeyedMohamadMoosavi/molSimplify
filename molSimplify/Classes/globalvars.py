## @file globalvars.py
## @file globalvars.py
#  Contains useful constants used throughout the code.
#  
#  Written by Tim Ioannidis for HJK Group
#  
#  Dpt of Chemical Engineering, MIT

import os, inspect, glob, platform, sys, subprocess
from math import sqrt

## Dictionary containing atomic mass, atomic number, covalent radius, number of valence electron
# Data from http://www.webelements.com/ (last accessed May 13th 2015)
amassdict = {'X': (1.0, 0, 0.77, 0), 'H': (1.0079, 1, 0.37, 1), 'He': (4.002602, 2, 0.46, 2),
             'Li': (6.94, 3, 1.33, 1), 'Be': (9.0121831, 4, 1.02, 2), 'B': (10.83, 5, 0.85, 3), 'C': (12.0107, 6, 0.77, 4),
             'N': (14.0067, 7, 0.75, 5), 'O': (15.9994, 8, 0.73, 6), 'F': (18.9984, 9, 0.71, 7), 'Ne': (20.1797, 10, 0.67, 0),
             'Na': (22.99, 11, 1.55, 1), 'Mg': (24.30, 12, 1.39, 2), 'Al': (26.98, 13, 1.26, 3), 'Si': (28.08, 14, 1.16, 4),
             'P': (30.9738, 15, 1.06, 5), 'S': (32.065, 16, 1.02, 6), 'Cl': (35.453, 17, 0.99, 7), 'Ar': (39.948, 18, 0.96, 0),
             'K': (39.10, 19, 1.96, 1), 'Ca': (40.08, 20, 1.71, 2),
             'Sc': (44.96, 21, 1.7, 3), 'Ti': (47.867, 22, 1.36, 4), 'V': (50.94, 23, 1.22, 5), 'Cr': (51.9961, 24, 1.27, 6),
             'Mn': (54.938, 25, 1.39, 7), 'Fe': (55.84526, 26, 1.25, 8), 'Co': (58.9332, 27, 1.26, 9), 'Ni': (58.4934, 28, 1.21, 10), 
             'Cu': (63.546, 29, 1.38, 11), 'Zn': (65.39, 30, 1.31, 2),
             'Ga': (69.72, 31, 1.24, 3), 'Ge': (72.63, 32, 1.21, 4), 'As': (74.92, 33, 1.21, 5), 'Se': (78.96, 34, 1.16, 6),
             'Br': (79.904, 35, 1.14, 7), 'Kr': (83.798, 36, 1.17, 0),
             'Rb': (85.47, 37, 2.10, 1), 'Sr': (87.62, 38, 1.85, 2),
             'Y': (88.91, 39, 1.63, 3), 'Zr': (91.22, 40, 1.54, 4), 'Nb': (92.91, 41, 1.47, 5), 'Mo': (95.96, 42, 1.38, 6),
             'Tc': (98.9, 43, 1.56, 7), 'Ru': (101.1, 44, 1.25, 8), 'Rh': (102.9, 45, 1.25, 9), 'Pd': (106.4, 46, 1.20, 10),
             'Ag': (107.9, 47, 1.28, 11), 'Cd': (112.4, 48, 1.48, 2),
             'In': (111.818, 49, 1.42, 3), 'Sn': (118.710, 50, 1.40, 4), 'Sb': (121, 760, 51, 1.40, 5), 'Te': (127.60, 52, 1.99, 6),
             'I': (126.90447, 53, 2.04, 7), 'Xe': (131.293, 54, 1.31, 0),
             'Cs': (132.9055, 55, 2.32, 1), 'Ba': (137.327, 56, 1.96, 2),
             'La': (138.9, 57, 1.69, 3), 'Ce': (140.116, 58, 1.63, 4), 'Pr': (140.90766, 59, 1.76, 5), 'Nd': (144.242, 60, 1.74, 6),
             'Pm': (145, 61, 1.73, 7), 'Sm': (150.36, 62, 1.72, 8), 'Eu': (151.964, 63, 1.68, 9), 'Gd': (157.25, 64, 1.69, 10),
             'Tb': (158.92535, 65, 1.68, 11), 'Dy': (162.500, 66, 1.67, 12), 'Ho': (164.93033, 67, 1.66, 13),
             'Er': (167.259, 68, 1.65, 14), 'Tm': (168.93422, 69, 1.64, 15), 'Yb': (173.045, 70, 1.70, 16),
             'Lu': (174.9668, 71, 1.62, 17),
             'Hf': (178.5, 72, 1.50, 4), 'Ta': (180.9, 73, 1.38, 5), 'W': (183.8, 74, 1.46, 6), 'Re': (186.2, 75, 1.59, 7),
             'Os': (190.2, 76, 1.28, 8), 'Ir': (192.2, 77, 1.37, 9), 'Pt': (195.1, 78, 1.23, 10), 'Au': (197.0, 79, 1.24, 11),
             'Hg': (200.6, 80, 1.49, 2),
             'Tl': (204.38, 81, 1.44, 3), 'Pb': (207.2, 82, 1.44, 4), 'Bi': (208.9804, 83, 1.51, 5),
             'Ra': (226.03, 88, 2.01, 2), 'Ac': (277, 89, 1.86, 3), 'Th': (232.0377, 90, 1.75, 4), 'U': (238.02891, 92, 1.70, 6)}

## van der Waals radii for commmon elements
# Data from http://www.webelements.com/ (last accessed May 13th 2015)
vdwrad = {'H': 1.2, 'C': 1.7, 'N': 1.55, 'O': 1.52, 'F': 1.47, 'P': 1.8, 'S': 1.8, 'Cl': 1.75, 'Br': 1.85, 'I': 1.98}

## Metals (includes alkali, alkaline earth, and transition metals)
metalslist = ['Li', 'li', 'LI', 'lithium', 'Be', 'be', 'BE', 'beryllium',
              'Na', 'na', 'NA', 'sodium', 'Mg', 'mg', 'MG', 'magnesium',
              'Al', 'al', 'AL', 'aluminum', 'aluminium',
              'K', 'k', 'potassium', 'Ca', 'ca', 'CA', 'calcium',
              'Rb', 'rb', 'RB', 'rubidium', 'Sr', 'sr', 'SR', 'strontium',
              'Cs', 'cs', 'CS', 'cesium', 'Ba', 'ba', 'BA', 'barium',
              'Fr', 'fr', 'FR', 'francium', 'Ra', 'ra', 'RA', 'radium', 
              'Sc', 'sc', 'SC', 'scandium', 'Ti', 'ti', 'TI', 'titanium', 
              'V', 'v', 'vanadium', 'Cr', 'cr', 'CR', 'chromium', 
              'Mn', 'mn', 'MN','manganese', 'Fe', 'fe', 'FE', 'iron', 
              'Co', 'co', 'CO', 'cobalt', 'Ni', 'ni', 'NI', 'nickel', 
              'Cu', 'cu', 'CU', 'copper', 'Zn', 'zn', 'ZN', 'zinc', 
              'Ga', 'ga', 'GA', 'gallium',
              'Y', 'y', 'yttrium', 'Zr', 'zr', 'ZR', 'zirconium', 
              'Nb', 'nb', 'NB', 'niobium', 'Mo', 'mo', 'MO', 'molybdenum', 
              'Tc', 'tc', 'TC', 'technetium', 'Ru', 'ru', 'RU', 'ruthenium', 
              'Rh', 'rh', 'RH', 'rhodium', 'Pd', 'pd', 'PD', 'palladium', 
              'Ag', 'ag', 'AG', 'silver', 'Cd', 'cd', 'CD', 'cadmium', 
              'In', 'in', 'IN', 'indium', 'Sn', 'sn', 'SN', 'tin',
              'Hf', 'hf', 'HF', 'hafnium', 'Ta', 'ta', 'TA', 'tantalum', 
              'W', 'w', 'tungsten', 'Re','re', 'RE', 'rhenium', 
              'Os', 'os', 'OS', 'osmium', 'Ir', 'ir', 'IR', 'iridium', 
              'Pt', 'pt', 'PT', 'platinum', 'Au', 'au', 'AU', 'gold', 
              'Hg', 'hg', 'HG', 'mercury', 
              'Tl', 'tl', 'TL', 'thallium', 'Pb', 'pb', 'PB', 'lead', 
              'Bi', 'bi', 'BI', 'bismuth', 'Po', 'po', 'PO', 'polonium',
              'La', 'la', 'LA', 'lanthanum',
              'Ce', 'ce', 'CE', 'cerium', 'Pr', 'pr', 'PR', 'praseodymium',
              'Nd', 'nd', 'ND', 'neodymium', 'Pm', 'pm', 'PM', 'promethium',
              'Sm', 'sm', 'SM', 'samarium', 'Eu', 'eu', 'EU', 'europium',
              'Gd', 'gd', 'GD', 'gadolinium','Tb', 'tb', 'TB', 'terbium',
              'Dy', 'dy', 'DY', 'dysprosium', 'Ho', 'ho', 'HO', 'holmium',
              'Er', 'er', 'ER', 'erbium', 'Tm', 'tm', 'TM', 'thulium',
              'Yb', 'yb', 'YB', 'ytterbium', 'Lu', 'lu', 'LU', 'lutetium',
              'Ac', 'ac', 'AC', 'actinium','Th', 'th', 'TH', 'thorium',
              'Pa', 'pa', 'PA', 'proactinium', 'U', 'u', 'uranium',
              'Np', 'np', 'NP', 'neptunium', 'Pu', 'pu','PU', 'plutonium',
              'Am', 'am', 'AM', 'americium', 'Cu', 'cu', 'CU', 'curium',
              'Bk', 'bk', 'BK', 'berkelium', 'Cf', 'cf', 'CF', 'californium',
              'Es', 'es', 'ES', 'einsteinium', 'Fm', 'fm', 'FM', 'fermium',
              'Md', 'md', 'MD', 'mendelevium', 'No', 'no', 'NO', 'nobelium',
              'Lr', 'lr', 'LR', 'lawrencium']

metals_conv = {'scandium':'Sc', 'titanium':'Ti', 'vanadium':'V', 'chromium':'Cr', 'manganese':'Mn',
               'iron':'Fe', 'cobalt': 'Co',  'nickel':'Ni',  'copper':'Cu',  'zinc':'Zn',
               'yttrium': 'Y', 'zirconium':'Zr', 'niobium': 'Nb', 'molybdenum':'Mo', 'technetium':'Tc', 
               'ruthenium':'Ru','rhodium': 'Rh', 'palladium':'Pd', 'silver':'Ag',  'cadmium':'Cd',
               'lanthanum':'La',  'hafnium':'Hf',
               'tantalum':'Ta', 'tungsten':'W', 
               'rhenium':'Re', 'osmium':'Os',
               'iridium':'Ir', 'platinum':'Pt',
               'gold': 'Au',  'mercury':'Hg'}
              
              
## d-electron counts of transition metals
mtlsdlist = {'sc': 1, 'ti': 2, 'v': 3, 'cr': 4, 'mn': 5, 'fe': 6, 'co': 7, 'ni': 8, 'cu': 9, 'zn': 10, 
             'y': 1, 'zr': 2, 'nb': 3, 'mo': 4, 'tc': 5, 'ru': 6, 'rh': 7, 'pd': 8, 'ag': 9, 'cd': 10, 
                     'hf': 2, 'ta': 3, 'w': 4, 're': 5, 'os': 6, 'ir': 7, 'pt': 8, 'au': 9, 'hg': 10}

## Default spins for each d-electron count (make this metal/oxidation state specific)
defaultspins = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '5', 7: '4', 8: '3', 9: '2', 10: '1'}

## Elements sorted by atomic number
elementsbynum = ['H', 'He', 
                 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 
                 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
                 'K', 'Ca',
                 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
                 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
                 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
                 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 
                 'Fr', 'Ra', 'Ac','Th','Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 
                 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Uut', 'Fl', 'Uup', 'Lv', 'Uus', 'Uuo']

## Electronegativity (Pauling) by atom symbol
endict = {"H": 2.20, 
          "Li": 0.98, "Be": 1.57, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44, "F": 3.98, 
          "Na": 0.93, "Mg": 1.31, "Al": 1.61, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16, 
          "K": 0.82, "Ca": 1.00, "Sc": 1.36, "Ti": 1.54, "V": 1.63, "Cr": 1.66,
          "Mn": 1.55, "Fe": 1.83, "Co": 1.88, "Ni": 1.91, "Cu": 1.90, "Zn": 1.65, "Ga": 1.81, 
          "Ge": 2.01, "As": 2.18, "Se": 2.55, "Br": 2.96, "Rb": 0.82, "Sr": 0.95, "Y": 1.22,
          "Zr": 1.33, "Nb": 1.60, "Mo": 2.16, "Tc": 2.10, "Ru": 2.20, "Rh": 2.28,
          "Pd": 2.20, "Ag": 1.93, "Cd": 1.69, "In": 1.78, "Sn": 1.96, "Sb": 2.05, "I": 2.66, 
          "Cs": 0.79, "Ba": 0.89, "Hf": 1.30, "Ta": 1.50, "W": 2.36, "Re": 1.90, "Os":2.20 ,"Ir": 2.20,
          "Pt": 2.28, "Au": 2.54, "Hg": 2.00, "Tl": 1.62, "Pb": 2.33, "Bi": 2.02,
          "La": 1.10, "Ce": 1.12, "Pr": 1.13, "Nd": 1.14, "Sm": 1.17,
          "Gd": 1.20, "Dy": 1.22, "Ho": 1.23, "Er": 1.24, "Tm": 1.25, "Lu": 1.27,
          "Fr": 0.7, "Ra": 0.9, "Ac": 1.1, "Th": 1.3, "Pa": 1.5, "U": 1.38, "Np": 1.36, "Pu": 1.28,
          "Am": 1.3, "Cm": 1.3, "Bk": 1.3, "Cf": 1.3, "Es": 1.3, "Fm": 1.3, "Md": 1.3, "No": 1.3 }
          

## Roman numerals
romans = {'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'VII': '7', 'VIII': '8'}

###---Geo_Check_Metrics------
dict_oct_check_loose = {'num_coord_metal': 6,
                        'rmsd_max': 0.4, 'atom_dist_max': 0.6,
                        'oct_angle_devi_max': 16, 'max_del_sig_angle': 27,
                        'dist_del_eq': 0.45, 'dist_del_all': 1.25,
                        'devi_linear_avrg': 35, 'devi_linear_max': 40}

dict_oct_check_st = {'num_coord_metal': 6,
                     'rmsd_max': 0.3, 'atom_dist_max': 0.45,
                     'oct_angle_devi_max': 12, 'max_del_sig_angle': 22.5,
                     'dist_del_eq': 0.35, 'dist_del_all': 1,
                     'devi_linear_avrg': 20, 'devi_linear_max': 28}  # default cutoff

dict_oneempty_check_st = {'num_coord_metal': 5,
                          'rmsd_max': 0.4, 'atom_dist_max': 0.7,
                          'oct_angle_devi_max': 15, 'max_del_sig_angle': 18,
                          'dist_del_eq': 0.5, 'dist_del_all': 1,
                          'devi_linear_avrg': 10, 'devi_linear_max': 20}

dict_oneempty_check_loose = {'num_coord_metal': 5,
                             'rmsd_max': 0.6, 'atom_dist_max': 0.9,
                             'oct_angle_devi_max': 20, 'max_del_sig_angle': 27,
                             'dist_del_eq': 0.6, 'dist_del_all': 1.2,
                             'devi_linear_avrg': 15, 'devi_linear_max': 28}

dict_tetra_check_loose = {'num_coord_metal': 4, 'rmsd_max': 0.4,
                          'oct_angle_devi_max': 16, 'max_del_sig_angle': 27,
                          'dist_del_all': 1.25,
                          'devi_linear_avrg': 35, 'devi_linear_max': 40}

dict_tetra_check_st = {'num_coord_metal': 4, 'rmsd_max': 0.3,
                       'oct_angle_devi_max': 12, 'max_del_sig_angle': 22.5,
                       'dist_del_all': 1,
                       'devi_linear_avrg': 20, 'devi_linear_max': 28}  # default cutoff

dict_staus = {'good': 1, 'bad': 0}

oct_angle_ref = [[90, 90, 90, 90, 180] for x in range(6)]
tetra_angle_ref = [[109.47, 109.47, 109.47] for x in range(4)]
oneempty_angle_ref = [[90, 90, 90, 90], [180, 90, 90, 90], [180, 90, 90, 90],
                      [180, 90, 90, 90], [180, 90, 90, 90]]
geo_check_dictionary = {"dict_oct_check_loose": dict_oct_check_loose,
                        "dict_oct_check_st": dict_oct_check_st,
                        "dict_oneempty_check_st": dict_oneempty_check_st,
                        "dict_oneempty_check_loose": dict_oneempty_check_loose,
                        "dict_staus": dict_staus,
                        "oct_angle_ref": oct_angle_ref,
                        "oneempty_angle_ref": oneempty_angle_ref}


## Module for running bash commands
#  @param cmd String containing command to be run
#  @return bash output string
def mybash(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)


## Defines global variables used throughout the code
class globalvars:
    ## Constructor
    #  @param self The object pointer
    def __init__(self):
        ## Program name
        self.PROGRAM = 'molSimplify'
        s = '\nmolSimplify v1.3.3x\nFreely distributed under the GNU GPL license.\n'
        s += 'Copyright 2017 Kulik Lab @ MIT\n'
        s += 'Developed by: Efthymios Ioannidis (timis@mit.edu)\n'
        s += 'Contributions by:\n\tHeather J. Kulik (hjkulik@mit.edu)\n'
        s += '\t Terry Gani (terryg@mit.edu)\n'
        s += '\t JP Janet (jpjanet@mit.edu)\n'
        s += 'E. I. Ioannidis, T. Z. H. Gani, H. J. Kulik. J. Comput. Chem. 2016, 37, 2106-2117.\n'
        s += 'J.P. Janet, Q. Zhao, E.I. Ioannidis, H.J. Kulik. Mol. Simul. 2017,43(5-6), 327-345.\n'
        s += 'J.P. Janet, T. Z. H. Gani, A. H. Steeves, E. I. Ioannidis, H. J. Kulik. Ind. Eng. Chem. Res. 2017, 56(17), 4898-4910.\n'
        ## About message
        self.about = s
        ###### GET INFORMATION ######
        runfromcmd, Linux, OSX = False, False, False
        try:
            ### check if running through commandline ###
            if sys.stdin.isatty():
                ## running through command line
                runfromcmd = True
            else:
                runfromcmd = False
        except:
            runfromcmd = True
        ### get running os ###
        if platform.system().lower() in 'linux':
            Linux = True
        elif platform.system().lower() in 'darwin':
            OSX = True
        self.osx = OSX
        ### get cwd
        cfile = inspect.getfile(inspect.currentframe())  # script filename (usually with path)
        cdir2 = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # script directory
        cdir = cdir2.rsplit('/', 1)[0]
        cdir2 = cdir
        homedir = os.path.expanduser("~")
        # create default molSimplify for mac
        if OSX and not glob.glob(homedir + '/.' + self.PROGRAM) and not runfromcmd:
            txt = 'INSTALLDIR=/Applications/' + self.PROGRAM + '.app/Contents/Resources\n'
            f = open(homedir + '/.' + self.PROGRAM, 'w')
            f.write(txt)
            f.close()
        self.chemdbdir = ''
        self.multiwfn = ''
        self.custom_path = False
        ###### check for ~/.molSimplify ######
        if glob.glob(homedir + '/.' + self.PROGRAM):
            f = open(homedir + '/.' + self.PROGRAM, 'r')
            s = filter(None, f.read().splitlines())
            d = dict()
            for ss in s:
                sp = filter(None, ss.split('='))
                try:
                    d[sp[0]] = sp[1]
                except:
                    pass
            if 'CHEMDBDIR' in d.keys():
                self.chemdbdir = d['CHEMDBDIR']
            if 'MULTIWFN' in d.keys():
                self.multiwfn = "'" + d['MULTIWFN'] + "'"
            if 'CUSTOM_DATA_PATH' in d.keys():
                self.custom_path = d['CUSTOM_DATA_PATH']
        else:
            self.installdir = cdir
            f = open(homedir + '/.' + self.PROGRAM, 'w')
            f.write('CHEMDBDIR=\n')
            f.close()

        ## Home directory
        self.homedir = homedir
        ## Number of smiles ligands
        self.nosmiles = 0
        ## Jobs directory
        self.rundir = homedir + '/Runs/'
        ## Number of generated structures
        self.generated = 0
        ## Additional debug output
        self.debug = False
        ## SMARTS patterns for forced hydrogen removal
        self.remHsmarts = ["O=CN", "O=CO", "n", "N=CN", "nN"]
        ## Default geometries for each coordination number if none specified
        self.defaultgeometry = {8: ('sqap', 'square_antiprismatic'), 7: ('pbp', 'pentagonal_bipyramidal'),
                                6: ('oct', 'octahedral'), 5: ('tbp', 'trigonal bipyramidal'), 4: ('thd', 'tetrahedral'),
                                3: ('trigonal planar', 'tpl'), 2: ('linear', 'li'), 1: ('one', 'one')}
        ## Default oxidation states for elements
        self.defaultoxstate = {'au': 'I', 'gold': 'I', 'scandium': 'III', 'sc': 'III', 'ti': 'IV', 'titanium': 'IV'}
        ## bent "linear" angle in degrees, e.g., in Fe(III)-superoxo or a bent nitrosyl
        self.linearbentang = 45

    ## Returns atomic mass dictionary
    #  @param self The object pointer
    #  @return Atomic mass dictionary
    def amass(self):
        return amassdict

    ## Returns metals list
    #  @param self The object pointer
    #  @return Metals list     
    def metals(self):
        return metalslist

    ## Returns list of elements by number
    #  @param self The object pointer
    #  @return List of elements by number             
    def elementsbynum(self):
        return elementsbynum

    ## Returns electronegativity dictionary
    #  @param self The object pointer
    #  @return Electronegativity dictionary        
    def endict(self):
        return endict

    ## Returns electronegativity dictionary
    #  @param self The object pointer
    #  @return Electronegativity dictionary 
    def vdwrad(self):
        return vdwrad

    ## Returns list of metals dictionary
    #  @param self The object pointer
    #  @return metals dictionary 
    def metalslist(self):
        return metalslist

    ## Returns list of geo check objects dictionary
    #  @param self The object pointer
    #  @return geo check objection  dictionary 
    def geo_check_dictionary(self):
        return geo_check_dictionary

    ## Record custom path in ~/.molSimplify file
    #  @param self The object pointer
    #  @param path Custom path 
    def add_custom_path(self, path):
        homedir = os.path.expanduser("~")
        f = open(homedir + '/.' + self.PROGRAM, 'a')
        f.write('CUSTOM_DATA_PATH=' + str(path) + "\n")
        f.close()

    ## Get backbone combinations dictionary
    #  @param self The object pointer    
    #  @return Backbone combinations dictionary
    def bbcombs_mononuc(self):
        bbcombs_mononuc = dict()
        bbcombs_mononuc['one'] = [[1]]
        bbcombs_mononuc['li'] = [[1], [2]]
        bbcombs_mononuc['oct'] = [[1, 2, 3, 4, 5, 6],  # 6-dentate
                                  [1, 2, 3, 4, 5], [1, 2, 3, 4, 6], [1, 2, 3, 5, 6], [1, 2, 4, 5, 6],  # 5-dentate
                                  [1, 3, 4, 5, 6], [2, 3, 4, 5, 6],  # 5-dentate
                                  [1, 2, 3, 4], [2, 5, 4, 6], [1, 5, 3, 6],  # 4-dentate
                                  [1, 2, 3], [1, 4, 2], [1, 4, 3], [1, 5, 3], [1, 6, 3], [2, 3, 4],  # 3-dentate
                                  [2, 5, 4], [2, 6, 4], [5, 4, 6], [5, 1, 6], [5, 2, 6], [5, 3, 6],  # 3-dentate
                                  [1, 2], [1, 4], [1, 5], [1, 6], [2, 3], [2, 5],  # 2-dentate
                                  [2, 6], [3, 5], [3, 6], [4, 5], [4, 6], [3, 4],  # 2-dentate
                                  [1], [2], [3], [4], [5], [6]]  # 1-dentate
        bbcombs_mononuc['pbp'] = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 6],  # 6/5-dentate
                                  [1, 2, 3, 5],  # 4-dentate
                                  [1, 2, 3], [1, 2, 4], [2, 1, 5], [3, 1, 6], [5, 6, 3], [2, 6, 5],  # 3-dentate
                                  [1, 2], [2, 3], [3, 4], [4, 5], [1, 7], [2, 6], [5, 7], [3, 6],  # 2-dentate
                                  [1], [2], [3], [4], [5], [6], [7]]  # 1-dentate
        bbcombs_mononuc['spy'] = [[1, 2, 3, 4, 5], [1, 2, 3, 4], [1, 2, 3], [2, 3, 4], [3, 4, 1], [4, 1, 2],
                                  [1, 2], [1, 4], [2, 3], [3, 4], [4, 5], [2, 5], [3, 5], [1, 5], [1], [2], [3], [4],
                                  [5]]
        bbcombs_mononuc['sqp'] = [[1, 4, 2, 3], [1, 2, 3], [2, 3, 4], [3, 4, 1], [4, 1, 2], [1, 2], [1, 4], [2, 3],
                                  [3, 4],
                                  [1], [2], [3], [4]]
        bbcombs_mononuc['tbp'] = [[1, 2, 3, 4, 5], [1, 3, 4, 5], [3, 2, 4], [4, 5, 3], [5, 1, 3], [4, 5], [5, 3],
                                  [3, 4],
                                  [1, 4], [1, 5], [1, 3], [2, 4], [2, 5], [2, 3], [1], [2], [3], [4], [5]]
        bbcombs_mononuc['thd'] = [[1, 2, 3, 4], [3, 2, 4], [2, 4, 1], [4, 1, 3], [2, 4], [4, 3], [3, 2], [1, 3], [1, 4],
                                  [2, 4], [1], [2], [3], [4]]
        bbcombs_mononuc['tpl'] = [[1, 2, 3], [1, 2], [2, 3], [1, 3], [1], [2], [3]]
        bbcombs_mononuc['tpr'] = [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 5], [1, 2, 5, 4], [5, 2, 3, 6], [1, 4, 6, 3],
                                  [1, 2, 3], [3, 6, 5],
                                  [2, 3], [2, 5], [5, 6], [6, 4], [4, 1], [1], [2], [3], [4], [5], [6]]
        return bbcombs_mononuc

    # Tests for keras/TF avail
    #  @return if keras/TF is avail
    def testTF(self):
        try:
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
            from keras.models import Model
            from keras.models import Sequential
            return True
        except:
            return False
