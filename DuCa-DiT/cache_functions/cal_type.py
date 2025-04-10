def cal_type(cache_dic, current):
    '''
    Determine calculation type for this step
    '''
    last_steps = (current['step'] <=2)
    first_step = (current['step'] == (current['num_steps'] - 1))
    force_fresh = cache_dic['force_fresh']
    if not first_step:
        fresh_interval = cache_dic['cal_threshold']
    else:
        fresh_interval = cache_dic['fresh_threshold']

    if (current['step'] % 6 == 0) or first_step:
        current['type'] = 'full'
        
    elif (current['step'] % 4 == 0): #[1,3,5] [2,4,6]
        current['type'] = 'ToCa'

    # 'aggressive' 'ToCa' 'FORA' 'Residual'
    elif current['step'] % 6 == 1:
        current['type'] = "skipped"
    else: 
        current['type'] = 'aggressive'
