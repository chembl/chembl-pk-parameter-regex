### I don't expect anyone to understand these regular expressions, even for me it became complicated.
### The complexity of the regex comes from the huge variety of different patterns they are expected to match
import re

dose_unit = re.compile(r'''(\()?\d+([\.|\-]\d+)?                                # dose value
                (\s* to \s*(\()?\d+([\.|\-]\d+)?)?                              # identify dose range
                \s*                                                             # there may be a whitespace
                (\()?                                                           # the unit may be put between parentheses. I know what you are thinking! Why?
                (micro\s)?([Mmnpu]?\s?[gLlmM](ol)?|[mnpu]?mol|[mnu]M|mpk|mgkg)  # it is X in X/Y units
                (\s+|$|,|.[Kk]g-1|.m-2|                                            # the unit may be only X
                /+                                                              # there may be more than one slash between x and Y
                \s*([Kkm]?g|pouch|m[Ll]|day|h(r)?|ear|rat))                     # it is Y in X/Y units
                (\))?                                                           # close the parenthese
                (/(min|h|day|kg))?                                              # sometimes the dose is indicated per minute or per day (X/Y/Z)
                ''', re.X)



time_of_measurement = re.compile(r'''\d+ \s mins \s to \s \d+ \s hrs                           # for any time intervals with a lower limit in `mins`, `to` as delimiter, and upper limit in `hours`                      
                                    |(
                                     (?<!\d)0(\.\d+)?(?:\s)?                                   # for time intervals starting at t=0 or t=0.something
                                         (to|-)(?:\s)?                                         # delimiter is `to` or `-`
                                             (\d+(\.\d+)?\s? (                                 # upper limit is a decimal
                                                             h(r)?(s)?                         # hours
                                                             |min(s)?                          # minutes
                                                             |day(s)?                          # days
                                                             ) |
                                                                 inf(init(y|ive))?             # infinity!
                                                                                 |last)        # `last` is not really informative but at least indicate a final time
                                     )
                                     (?!\s?(mg|year|MBq))                                      # the unit must not be mg or year or MBq
                                    | \d+(\.\d+)? (\s h(r)?(s)?|-\d+) \s (?=after)             # time intervals followed by `after`
                                    | (
                                        (up(\s)?to)                                            # time intervals following `upto`                 
                                        |after                                                 # or `after`
                                        |over                                                  # or `during`
                                        |during)\s                                             # or `over`
                                            \d+(\.\d+)? \s (                                   # time is a decimal
                                                            h(r)?(s)?                          # hours
                                                                | min(s)?)                     # mins
                                                                    (\s to\s \d+\s (hr(s)?     #
                                                                                    |min(s)?   #
                                                                                        ))?    #
                                    | AUC                                                      # time following `AUC`                      
                                         ( (\s)? inf(inity)?                                   # infinity
                                             | (\s)? last(?!(.*)(after|up\s?to))               # last but not followed by `after` or `up to`
                                             | max                                             # max
                                             | tau                                             # tau?
                                             | tot(al)?                                        # total
                                             | (\s)? \(                                        # opening parentheses
                                                    ((\d+|o)\s(to\s?)? (\d+)?\s?               # time is a decimal
                                                                             (h)?(r)?(s)?      # hours  
                                                                             |inf(inity)?      # infinity
                                                                             |last             # last
                                                                             )            
                                                                             \))               # closing parentheses
                                    | AUC\s \(0-(\d+)\)(hrs)?                                  # could be merged with the previous pattern
                                    | at\s                                                     # time following `at`
                                        \d+((\s hr(s)?)(?!\s interval)                         # time is a decimal and is in hours
                                        |(.5,\s 1,\s 2,\s and\s 4\s hour\s after\s dosing))    # very specific case
                                    | infinite \s hours                                        # another specific case
                                    | from\s zero\s time\s to\s                                # another specific case
                                            (24\s hr                                           # another specific case
                                            | infinity
                                            | time\s of\s last\s detectable\s concentration
                                            )
                                    | total \s AUC                                             # another specific case

                            ''', re.I | re.X)


# How the compound was administrated
route_of_administration = re.compile(r'''\b
                                        (?: i 
                                            (?: ntra
                                                (?: cerebroventricular (?:ly)?
                                                  | duodenal (?:ly)?
                                                  | gastric (?:ally)?
                                                  | jejunal
                                                  | muscular (?:ly)?
                                                  | nasal (?:ly)?
                                                  | ocular(?:ly)?
                                                  | oral (?:ally)?
                                                  | peritoneal (?:ly)?
                                                  | topical (?:ly)?
                                                  | tumoral
                                                  | venous (?:ly)?
                                                ) \b
                                              | \.? (?: [gmpv](?!\-) | c \.? v ) \b \.?
                                            )
                                          |
                                            inhala(?:ble|tion)? \b
                                          |
                                            \sit (?:measured)? \b
                                          |
                                            nasogastric \b
                                          |
                                            (?:par|per|pre)? oral (?:ly)? \b
                                          |
                                            p \.? o \b \.?
                                          |
                                            s
                                             (?: c
                                             | ubcutaneous (?:ly)? (?: \s+ injection )?
                                             | ublingual
                                             ) \b
                                          |
                                            (?:to|per)? (?:each|both)? eye(?:s)? \b
                                        )''', re.I | re.X)

# From which tissue the PKPD parameter is measured
tissue = re.compile(r'''\b
                        (?:
                        alveolar \s cell 
                        |biliary \s fluid
                        |blood
                        |body \s fluid
                        |brain
                        |cage \s fluid
                        |cerebrospinal  \s  fluid
                        |choroid
                        |cornea
                        |csf
                        |(?: lung\s)? epithelial \s lining \s fluid
                        |extracellular \s fluid
                        |\s fat \s (?! fed|meal|diet)
                        |heart
                        |hypothalamus
                        |interstitial \s fluid
                        |(?: interstitial-space \s fluid \s of \s subcutaneous \s)? adipose \s tissue
                        |(?:large\s|small\s)? intestine
                        |jejunum
                        |kidney (?! \sdisease|\stransplant|\sinjury)
                        |liver (?! \simpairment|\stransplant|\sinjury)
                        |lung (?! \scancer|\stransplant)
                        |mesenteric \s lymph (?! \sduct-cannulated)
                        |muscle
                        |peritoneal \s fluid
                        |plasma
                        |portal \s vein
                        |prostate
                        |retina
                        |sciatic \s nerve
                        |serum
                        |skin
                        |spleen
                        |stomach
                        |thigh
                        |tumor
                        |(?:\s)? urine
                        ) \b
                      ''', re.I | re.X)


def find_dose_unit(dose_unit, description):
    m = re.search(dose_unit, description)
    if m != None:
        return(m.group(0))
    else:
        return(None)

def find_route(route_of_administration, description):
    m = re.findall(route_of_administration, description)
    return(' | '.join(set(m)))

def find_time(time, description):
    m = re.search(time, description)
    if m != None:
        return(m.group(0))
    else:
        return(None)

def find_tissue(tissue, description):
    m = re.findall(tissue, description)
    if len(m) == 2:
        n = [s.lower() for s in m]
        if 'plasma' in n:
            return('plasma')
        elif 'extracellular fluid' in n:
            return('extracellular fluid')
        else:
            return(' | '.join(set(n)))
    else:   
        return(' | '.join(set(m)))

def split_dose_unit(s):
    if s:
        try:
            s = s.replace('(','').replace(')','').strip().strip(',')
            s = s.replace('mg.Kg-1','mg/kg')
            s = s.replace('mg.m-2','mg/m2')
            s = s.replace('mg/ kg', 'mg/kg')
            s = re.sub('\s+',' ',s) # remove double splaces
            if ' ' in s:
                return s.split(' ')[0], s.split(' ')[1]
            else: # value and unit have no space between them
                s= re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", s).strip() 
                return s.split(' ')[0], s.split(' ')[1]
        except TypeError:
            return None, None
    else:
        return None, None

def remove_low_quality_pk_data(df
#                                , keep_missing_standard_value=True
                               , keep_ambiguous_route=False
                               , keep_ambiguous_tissue=False
                               , keep_missing_dose=True):
    '''
    PK data are low quality when some of the parameters where not correctly extracted
    or when there is an ambiguity on them due to the curation or the original data themself
    '''
    print('DATA FILTERING - START\n')
    print(f'Before curation, there are {len(df)} {df.standard_type.unique()[0]} data points.')

    if not keep_ambiguous_route:
        print('{} {} data points have an ambiguous route of administration and were excluded.'.format(len(df[df.route.str.contains(" \| ")]), df.standard_type.unique()[0]))
        df = df[~df.route.str.contains(' \| ')]
    else:
        print('{} {} data points have an ambiguous route of administration but were kept.'.format(len(df[df.route.str.contains(" \| ")]), df.standard_type.unique()[0]))

    if not keep_missing_dose:
        print(f'{len(df[df.dose_unit.isnull()])} {df.standard_type.unique()[0]} data points have no dose information and were excluded.')
        df= df[~df.dose_unit.isnull()]
    else:
        print(f'{len(df[df.dose_unit.isnull()])} {df.standard_type.unique()[0]} data points have no dose information but were kept.')        
    
    print(f'{len(df[df.dose_unit.str.contains("to", na=False)])} {df.standard_type.unique()[0]} data points have a dose range and they have been excluded.')
    df = df[~df.dose_unit.str.contains('to', na=False)]

    if 'time' in df.columns:
        # fix times incorrectly identified
        df['time'] = df['time'].replace(['0 to 12 '],None)
        df['time'] = df['time'].replace(['0.19-0.35'],None)
        df['time'] = df['time'].replace(['0.01 to 0.0'],'24 hrs')
        df['time'] = df['time'].replace(['0.25 to 2'],'24 hrs')
        df['time'] = df['time'].replace(['0.075 to 0.2'],'24 hrs')
        df['time'] = df['time'].replace(['0.37 to 1.85 '],None)
        # fix data
        df.loc[df.activity_id==1425305,'time']='0-4 h'
        df.loc[df.activity_id==19054467, 'time']='up to 24 hrs'
        df.loc[df.activity_id==7927654, 'time']='0 to infinity'
        
        print(f'{len(df[df.time.isnull()])} {df.standard_type.unique()[0]} data points have no time and they have been excluded')
        df = df[~df.time.isnull()]
    
    unwanted_cmax_activities = [2571867,501336, 555209, 1277556, 1292783,1294137, 1288807, 555215,
                                560993, 573255, 585466, 579341, 580553, 555209, 580547, 564568,
                                575619, 563404, 568168, 560073, 587892, 586691, 555215, 557585,
                                558774, 585456, 581717, 569515, 13429985, 13429986
                               ]
    unwanted_auc_activities = [17994450
                              ]
    
    df = df[~df.activity_id.isin(unwanted_cmax_activities+unwanted_auc_activities)]
    
#     df['dose'], df['unit'] = zip(*df.dose_unit.apply(lambda x: split_dose_unit(x)))
    
    print(f'After curation, there are now {len(df)} {df.standard_type.unique()[0]} data points')
    
    print('\nDATA FILTERING - END')

    return(df)