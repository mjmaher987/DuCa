def cal_type(cache_dic, current):
    '''
    Return whether to force fresh tokens globally.
    '''
    types = {}
    fresh_thresholds = {}
    first_step = (current['step'] == 0)
    first_3steps = (current['step'] <= 2) # Note the fact that for OpenSora series models, the first 3 steps is with great importance!!!
    last_step = current['step'] == current['num_steps'] - 1
    force_fresh = cache_dic['force_fresh']
    if not first_step:
        fresh_thresholds['spat-attn']  = cache_dic['cal_threshold']['spat-attn']
        fresh_thresholds['temp-attn']  = cache_dic['cal_threshold']['temp-attn']
        fresh_thresholds['cross-attn'] = cache_dic['cal_threshold']['cross-attn']
        fresh_thresholds['mlp']        = cache_dic['cal_threshold']['mlp']
    else:
        fresh_thresholds['spat-attn']  = cache_dic['fresh_threshold']
        fresh_thresholds['temp-attn']  = cache_dic['fresh_threshold']
        fresh_thresholds['cross-attn'] = cache_dic['fresh_threshold']
        fresh_thresholds['mlp']        = cache_dic['fresh_threshold']

    if force_fresh == 'global':
        inter_list = ['ToCa', 'aggressive']
        lists_ToCa_CN = {'temp-attn':   ['full', 'ToCa', 'aggressive', 'full', 'ToCa', 'aggressive'],
                         'spat-attn':   ['full', 'ToCa', 'aggressive', 'full', 'ToCa', 'aggressive'],
                         'cross-attn':  ['full', 'ToCa', 'aggressive', 'ToCa', 'ToCa', 'aggressive'],
                         'mlp':         ['full', 'ToCa', 'aggressive', 'full', 'ToCa', 'aggressive']
        }
        lists_ToCa =    {'temp-attn':   ['full', 'ToCa', 'ToCa',        'full', 'ToCa', 'ToCa'       ],
                         'spat-attn':   ['full', 'ToCa', 'ToCa',        'full', 'ToCa', 'ToCa'       ],
                         'cross-attn':  ['full', 'ToCa', 'ToCa',        'ToCa', 'ToCa', 'ToCa'       ],
                         'mlp':         ['full', 'ToCa', 'ToCa',        'full', 'ToCa', 'ToCa'       ]
        }
        lists_CN =      {'temp-attn':   ['full', 'aggressive', 'aggressive', 'full', 'aggressive', 'aggressive'],
                         'spat-attn':   ['full', 'aggressive', 'aggressive', 'full', 'aggressive', 'aggressive'],
                         'cross-attn':  ['full', 'aggressive', 'aggressive', 'full', 'aggressive', 'aggressive'],
                         'mlp':         ['full', 'aggressive', 'aggressive', 'full', 'aggressive', 'aggressive']
        }
        lists_full =    {'temp-attn':   ['full', 'full', 'full', 'full', 'full', 'full'],
                         'spat-attn':   ['full', 'full', 'full', 'full', 'full', 'full'],
                         'cross-attn':  ['full', 'full', 'full', 'full', 'full', 'full'],
                         'mlp':         ['full', 'full', 'full', 'full', 'full', 'full']
        }
        lists_test=     {'temp-attn':   ['full', 'aggressive', 'aggressive', 'aggressive', 'aggressive', 'aggressive'],
                         'spat-attn':   ['full', 'aggressive', 'aggressive', 'aggressive', 'aggressive', 'aggressive'],
                         'cross-attn':  ['full', 'aggressive', 'aggressive', 'aggressive', 'aggressive', 'aggressive'],
                         'mlp':         ['full', 'aggressive', 'aggressive', 'aggressive', 'aggressive', 'aggressive']
        }
        lists = lists_ToCa_CN

        if current['flag'] == -1:
            if (first_3steps or (current['step']% fresh_thresholds['temp-attn'] == 0)):
                types['attn']   =   lists['temp-attn'][0]
            else:
                types['attn']   =   lists['temp-attn'][current['step']% fresh_thresholds['temp-attn']]

        else:
            if (first_3steps or (current['step']% fresh_thresholds['spat-attn'] == 0)):
                types['attn']   =   'full'
            else:
                types['attn']   =   lists['spat-attn'][current['step']% fresh_thresholds['spat-attn']]

        if (first_3steps or (current['step']% fresh_thresholds['cross-attn'] == 0)):
            types['cross-attn'] = 'full'
        else:
            types['cross-attn'] =   lists['cross-attn'][current['step']% fresh_thresholds['cross-attn']]

        if (first_3steps or (current['step']% fresh_thresholds['mlp'] == 0)):
            types['mlp']        =  'full'
        else:
            types['mlp']        =   lists['mlp'][current['step']% fresh_thresholds['mlp']]
        

        types['all_aggressive'] =       (types['attn']       == 'aggressive')\
                                    and (types['cross-attn'] == 'aggressive')\
                                    and (types['mlp']        == 'aggressive')

        return types
    
    elif force_fresh == 'local':
        return first_step
    elif force_fresh == 'none':
        return first_step
    else:
        raise ValueError("unrecognized force fresh strategy", force_fresh)