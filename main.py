from copy import deepcopy
import datetime, json, math, numpy, os, sys
import matplotlib.pyplot as pyplot
import pdfreader # https://pdfreader.readthedocs.io/en/latest/
import PyInquirer # https://github.com/CITGuru/PyInquirer

CAPSIM_START_YEAR : int = 2022
CAPSIM_GAME_ID : str = 'C133749'
CAPSIM_TEAM_NAME : str = 'Andrews'

SEGMENT_INFO : dict = {
    'total_industry_unit_demand': [ ],
    'actual_industry_unit_sales': [ ],
    'segment_percent_of_total_industry': [ ],
    'next_year_segment_growth_rate': [ ],

    'customer_buying_criteria': {
        'ideal_age': {
            'value': [ ],
            'importance': [ ]
        },
        'price': {
            'value': {
                'min': [ ],
                'max': [ ]
            },
            'importance': [ ]
        },
        'ideal_position': {
            'value': {
                'pfmn': [ ],
                'size': [ ]
            },
            'importance': [ ]
        },
        'mtbf': {
            'value': {
                'min': [ ],
                'max': [ ]
            },
            'importance': [ ]
        },
    }
}

MARKET_SEGMENTS : dict = { 
    'Trad': deepcopy(SEGMENT_INFO), 
    'Low': deepcopy(SEGMENT_INFO), 
    'High': deepcopy(SEGMENT_INFO), 
    'Pfmn': deepcopy(SEGMENT_INFO), 
    'Size': deepcopy(SEGMENT_INFO) 
}

PRODUCT_INFO : dict = {
    'product_name': '{product_name}',
    'primary_segment': '{primary_segment}',

    'production_analysis': {
        'units_sold': [ ],
        'unit_inventory': [ ],
        'revision_date': [ ],
        'age_dec_31': [ ],
        'mtbf': [ ],
        'pfmn_coord': [ ],
        'size_coord': [ ],
        'price': [ ],
        'material_cost': [ ],
        'labor_cost': [ ],
        'contribution_margin': [ ],
        '2nd_shift_and_overtime': [ ],
        'automation_next_round': [ ],
        'capacity_next_round': [ ],
        'plant_utilization': [ ]
    },

    'segment_analysis': {
        'market_share': [ ],
        'units_sold_to_seg': [ ],
        'revision_date': [ ],
        'pfmn_coord': [ ],
        'size_coord': [ ],
        'list_price': [ ],
        'mtbf': [ ],
        'age_dec_31': [ ],
        'promo_budget': [ ],
        'customer_awareness': [ ],
        'sales_budget': [ ],
        'customer_accessibility': [ ],
        'customer_survery_score': [ ]
    },
    
#    'market_share': {
#        'actual': {
#            'trad': [ ],
#            'low': [ ],
#            'high': [ ],
#            'pfmn': [ ],
#            'size': [ ],
#            'total': [ ]
#        },
#        'potential': {
#            'trad': [ ],
#            'low': [ ],
#            'high': [ ],
#            'pfmn': [ ],
#            'size': [ ],
#            'total': [ ]
#        },
#    }
}

COMPANY_INFO : dict = {
    'selected_financial_stats': {
        'return_on_sales': [ ],
        'asset_turnover': [ ],
        'return_on_assets': [ ],
        'leverage': [ ],
        'return_on_equity': [ ],
        'emergency_loan': [ ],
        'sales': [ ],
        'ebit': [ ],
        'profits': [ ],
        'cumulative_profit': [ ],
        'sga_sales': [ ],
        'contribution_margin': [ ]
    },
    'stock': {
        'close': [ ],
        'change': [ ],
        'shares': [ ],
        'market_cap': [ ],
        'book_value_per_share': [ ],
        'earnings_per_share': [ ],
        'dividend': [ ],
        'yield_percent': [ ],
        'price_to_earnings': [ ]
    },
    'products': {
        # filled in when analyzing production analysis
        # 'product_name': copy(PRODUCT_INFO),
    },
    'financial': {
        'net_income': [ ],
        'adj_depreciation': [ ],
        'adj_extraordinary': [ ],
        'changes_accounts_payable': [ ],
        'changes_accounts_receivable': [ ],
        'changes_inventory': [ ],
        'net_cash_operations': [ ],
        'plant_improvements': [ ],
        'dividends_paid': [ ],
        'sales_common_stock': [ ],
        'purchase_common_stock': [ ],
        'long_term_debt_issued': [ ],
        'long_term_debt_early_retire': [ ],
        'current_debt_retirement': [ ],
        'current_debt_borrowing': [ ],
        'emergency_loan_paid': [ ],
        'net_cash_financing': [ ],
        'net_change_cash_position': [ ],
        'cash': [ ],
        'accounts_receivable': [ ],
        'inventory': [ ],
        'total_current_assets': [ ],
        'plant_and_equipment': [ ],
        'accumulated_depreciation': [ ],
        'total_fixed_assets': [ ],
        'total_assets': [ ],
        'accounts_payable': [ ],
        'current_debt': [ ],
        'total_current_liabilities': [ ],
        'long_term_debt': [ ],
        'total_liabilities': [ ],
        'common_stock': [ ],
        'retained_earnings': [ ],
        'total_equity': [ ],
        'total_liabilities_and_owners_equity': [ ],
        'sales': [ ],
        'variable_costs': [ ],
        'contribution_margin': [ ],
        'depreciation': [ ],
        'sga': [ ],
        'other': [ ],
        'ebit': [ ],
        'interest': [ ],
        'taxes': [ ],
        'profit_sharing': [ ],
        'net_profit': [ ]
    },
    'human_resources': {

    },
    'tqm': {
        'cpi_systems': [ ],
        'vendorjit': [ ],
        'quality_initiative_training': [ ],
        'channel_support_systems': [ ],
        'concurrent_engineering': [ ],
        'unep_green_programs': [ ],
        
        'benchmarking': [ ],
        'quality_function_deployment_effort': [ ],
        'cce6_sigma_training': [ ],
        'gemi_tqem': [ ],
        'total_expenditures': [ ],
        
        'material_cost_reduction': [ ],
        'labor_cost_reduction': [ ],
        'reduction_rd_cycle_time': [ ],
        'reduction_admin_costs': [ ],
        'demand_increase': [ ]
    }
}

COMPANIES : dict = {
    'Andrews': deepcopy(COMPANY_INFO),
    'Baldwin': deepcopy(COMPANY_INFO),
    'Chester': deepcopy(COMPANY_INFO),
    'Digby': deepcopy(COMPANY_INFO),
    'Erie': deepcopy(COMPANY_INFO),
    'Ferris': deepcopy(COMPANY_INFO)
}

COMPANY_PRODUCT_MAP : dict = {
    'A': 'Andrews',
    'B': 'Baldwin',
    'C': 'Chester',
    'D': 'Digby',
    'E': 'Erie',
    'F': 'Ferris'
}

INCOME_STATEMENT_ITEM : dict = {
    'sales': [ ],
    'direct_labor': [ ],
    'direct_material': [ ],
    'inventory_carry': [ ],
    'total_variable_costs': [ ],
    'contribution_margin': [ ],
    'depreciation': [ ],
    'sga_rnd': [ ],
    'sga_rnd_promotions': [ ],
    'sga_rnd_sales': [ ],
    'sga_rnd_admin': [ ],
    'total_period_costs': [ ],
    'net_margin': [ ],
    # the following are only used by summary items
    'other': [ ],
    'ebit': [ ],
    'short_term_interest': [ ],
    'long_term_interest': [ ],
    'taxes': [ ],
    'profit_sharing': [ ],
    'net_profit': [ ]
}

ANNUAL_REPORT : dict = {
    'income_statement': {
        # your teams products are copied here
        # 'product_name': copy(INCOME_STATEMENT_ITEM)
        # along with the following summary items
        'year_total': deepcopy(INCOME_STATEMENT_ITEM),
        'common_size': deepcopy(INCOME_STATEMENT_ITEM)
    }
}

CONSOLE_STYLE = PyInquirer.style_from_dict({
    PyInquirer.Token.Separator: '#cc5454',
    PyInquirer.Token.QuestionMark: '#673ab7 bold',
    PyInquirer.Token.Selected: '#cc5454', # default
    PyInquirer.Token.Pointer: '#673ab7 bold',
    PyInquirer.Token.Instruction: '', # default
    PyInquirer.Token.Answer: '#f44336 bold',
    PyInquirer.Token.Question: '',
})

JSON_EXT : str = '.cx.json'
NULL_STR : str = 'n/a'
MAX_NUM_ROUNDS : int = 8
DATE_FORMAT : str = '%m/%d/%Y'
PAGE_TERMINATOR : str = 'CAPSTONE ® COURIER'
ABCDEF : list = [ 'A', 'B', 'C', 'D', 'E', 'F' ]

IS_FILE_EXT = lambda file_path, file_ext: os.path.splitext(file_path)[-1].lower() == file_ext.lower()

def get_next_str(raw : list, start : int):
    for index in range(start, len(raw)):
        if raw[index] in COMPANIES.keys():
            # company names
            return index + 1, raw[index]
        elif len(raw[index]) >= 3 and raw[index][0:1] in ABCDEF:
            # product names
            return index + 1, raw[index]
            # product segments
        elif raw[index] in MARKET_SEGMENTS.keys():
            return index + 1, raw[index]
    return start + 1, NULL_STR

def get_next_val(raw : list, start : int):
    for index in range(start, len(raw)):
        raw_str = raw[index]
        if raw_str == '0':
            return index + 1, 0
        elif raw_str == '0.0' or raw_str == '$0.00' or raw_str == '0%':
            return index + 1, 0.0
        elif raw_str[-1:] == '%':
            # percent value
            return index + 1, float(raw_str[0:-1]) / 100
        elif raw_str[0] == '(':
            # negative dollar value
            return index + 1, -1 * float('0' + raw_str.replace(',', '')[2:-1])
        elif raw_str[0] == '$':
            # positive dollar value
            return index + 1, float('0' + raw_str.replace(',', '')[1:])
        else:
            # datetime value
            try:
                return index + 1, datetime.datetime.strptime(raw_str, DATE_FORMAT).strftime(DATE_FORMAT)
            except:
                # base case: float/int value
                # if it's not this then it's nothing useful
                try:
                    value = raw_str.replace(',', '')
                    return index + 1, '.' in value and float(value) or int(value)
                except:
                    pass
    return start + 1, -1

def load_folder(folder_path : str):
    global ANNUAL_REPORT
    global COMPANIES
    global MARKET_SEGMENTS
    # step 1: collect & organize
    raw : list = None
    index : int = None 
    value : int | float | datetime.datetime = None
    viewer : pdfreader.SimplePDFViewer = None
    file_count : int = 0
    round_years : list = [ ]
    round_numbers : list = [ ]
    # start scan on input directory
    for file_path in os.scandir(folder_path):
        # skip over non pdf files
        if not IS_FILE_EXT(file_path, '.pdf'):
            print('Skipping file: {0}'.format(file_path))
            continue
        # open next capstone courier pdf file
        with open(file_path, 'rb') as file:
            company_name : str = NULL_STR
            company_data : dict = None
            # create pdf viewer object for courier file
            viewer = pdfreader.SimplePDFViewer(file)
            # selected financial stats page
            viewer.navigate(1)
            viewer.render()
            raw = viewer.canvas.strings
            # first, get the round number & year
            this_round : int = int(raw[0][-1:])
            if this_round == 0:
                print('Found file for Round Zero. Ignoring')
                file.close()
                continue
            this_year : int = int(raw[2])
            round_numbers.append(this_round)
            round_years.append(this_year)
            print('Processing Capstone Courier: Round {0}, Year {1}'.format(this_round, this_year))
            # start data collection
            index = raw.index(' ROS') + 1
            #print('> selected financial stats')
            for category in COMPANY_INFO['selected_financial_stats'].keys():
                for company_name in COMPANIES.keys():
                    index, value = get_next_val(raw, index)
                    company_fstats = COMPANIES[company_name]['selected_financial_stats']
                    company_fstats[category].append(value)
                index += 1
            # stock market summary page
            viewer.navigate(2)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index('P/E') + 1
            #print('> stock summary')
            for company_name in COMPANIES.keys():
                index = raw.index(company_name)
                company_stock = COMPANIES[company_name]['stock']
                for category in company_stock.keys():
                    index, value = get_next_val(raw, index)
                    if not value == -1:
                        company_stock[category].append(value)
                        #print(company_name, category, [this_year, value])
            # financial summary page
            viewer.navigate(3)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index(' Net Income(Loss)') + 1
            #print('> finance summary')
            for category in COMPANY_INFO['financial'].keys():
                for company_name in COMPANIES.keys():
                    index, value = get_next_val(raw, index)
                    company_finc = COMPANIES[company_name]['financial']
                    if not value == -1:
                        company_finc[category].append(value)
                        #print(company_name, category, [this_year, value])
            # production analysis page
            viewer.navigate(4)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index('Utiliz.') + 1
            # product specs
            primary_seg : str = NULL_STR
            product_name : str = NULL_STR
            #print('> production analysis')
            while index < len(raw) and not raw[index] == PAGE_TERMINATOR:
                index, product_name = get_next_str(raw, index)
                if raw[index] == '0' and raw[index + 1] == '0':
                    # this is a new product,
                    # it has no primary segment yet
                    primary_seg = NULL_STR
                else:
                    index, primary_seg = get_next_str(raw, index)
                company_name = COMPANY_PRODUCT_MAP[product_name[0:1]]
                company_data = COMPANIES[company_name]
                company_products = company_data['products']
                product_data : dict = None
                # create new product for company - if not exists
                if not product_name in company_products.keys():
                    product_data = deepcopy(PRODUCT_INFO)
                    company_products[product_name] = product_data
                    product_data['product_name'] = product_name
                    product_data['primary_segment'] = primary_seg
                else:
                    product_data = company_products[product_name]
                    if not product_data['primary_segment'] == primary_seg:
                        product_data['primary_segment'] = primary_seg
                for category in PRODUCT_INFO['production_analysis'].keys():
                    index, value = get_next_val(raw, index)
                    product_analysis = product_data['production_analysis']
                    if not value == -1:
                        product_analysis[category].append(value)
                    else:
                        print(company_name, product_name, category, this_year, index, value)
                        print(raw)
                        exit()
            #print('> segment analysis')
            category : dict = None
            page_number : int = 5
            # stats & customer criteria
            splice : int = 0
            min_splice : int = 0
            max_splice : int = 0
            pfmn_splice : int = 0
            size_splice : int = 0
            importance : float = 0.0
            expectation : float = 0.0
            min_expectation : float = 0.0
            max_expectation : float = 0.0
            pfmn_expectation : float = 0.0
            size_expectation : float = 0.0
            # begin iterating thru each market segment page
            for market_segment in MARKET_SEGMENTS.keys():
                market_seg_data = MARKET_SEGMENTS[market_segment]
                # nav to next market segment
                viewer.navigate(page_number)
                viewer.render()
                raw = viewer.canvas.strings
                # market stats
                index = raw.index(' Total Industry Unit Demand') + 1
                value = int(raw[index].replace(',', '').replace('|', ''))
                market_seg_data['total_industry_unit_demand'].append(value)
                index = raw.index(' Actual Industry Unit Sales') + 1
                value = int(raw[index].replace(',', '').replace('|', ''))
                market_seg_data['actual_industry_unit_sales'].append(value)
                index = raw.index(' Segment % of Total Industry') + 1
                value = float(raw[index][0:-1].replace(',', '').replace('|', '')) / 100
                market_seg_data['segment_percent_of_total_industry'].append(value)
                index = raw.index("Next Year's Segment Growth Rate") + 1
                value = float(raw[index][0:-1].replace(',', '').replace('|', '')) / 100
                market_seg_data['next_year_segment_growth_rate'].append(value)
                # customer buying criteria
                # capsim seems to mix the order of these between each segment
                # bruteforce the order for convenience
                criteria_order : list = [ '1', '2', '3', '4' ]
                # age
                category = market_seg_data['customer_buying_criteria']['ideal_age']
                for criteria_num in criteria_order:
                    try:
                        index = raw.index(criteria_num + '. Age') + 1
                        splice = raw[index].index('= ')
                        expectation = float(raw[index][splice+2:len(raw[index])])
                        importance = float(raw[index + 1][0:-1]) / 100
                        category['value'].append(expectation)
                        category['importance'].append(importance)
                        criteria_order.remove(criteria_num)
                        #print(market_segment, criteria_num + '. Age', expectation, importance)
                    except:
                        pass
                # price
                category = market_seg_data['customer_buying_criteria']['price']
                for criteria_num in criteria_order:
                    try:
                        index = raw.index(criteria_num + '. Price') + 1
                        min_splice = raw[index].index('$')
                        max_splice = raw[index].index('- ')
                        min_expectation = float(raw[index][min_splice+1:max_splice])
                        max_expectation = float(raw[index][max_splice+2:len(raw[index])])
                        importance = float(raw[index + 1][0:-1]) / 100
                        category['value']['min'].append(min_expectation)
                        category['value']['max'].append(max_expectation)
                        category['importance'].append(importance)
                        criteria_order.remove(criteria_num)
                    except:
                        pass
                # ideal positions
                category = market_seg_data['customer_buying_criteria']['ideal_position']
                for criteria_num in criteria_order:
                    try:
                        index = raw.index(criteria_num + '. Ideal Position') + 1
                        pfmn_splice = raw[index].index('Pfmn ')
                        size_splice = raw[index].index('Size ')
                        pfmn_expectation = float(raw[index][pfmn_splice+5:size_splice-1])
                        size_expectation = float(raw[index][size_splice+5:len(raw[index])])
                        importance = float(raw[index + 1][0:-1]) / 100
                        category['value']['pfmn'].append(pfmn_expectation)
                        category['value']['size'].append(size_expectation)
                        category['importance'].append(importance)
                        criteria_order.remove(criteria_num)
                    except:
                        pass
                # reliability (MTBF)
                category = market_seg_data['customer_buying_criteria']['mtbf']
                for criteria_num in criteria_order:
                    try:
                        index = raw.index(criteria_num + '. Reliability') + 1
                        min_splice = raw[index].index(' ')
                        max_splice = raw[index].index('-')
                        min_expectation = int(raw[index][min_splice+1:max_splice])
                        max_expectation = int(raw[index][max_splice+1:len(raw[index])])
                        importance = float(raw[index + 1][0:-1]) / 100
                        category['value']['min'].append(min_expectation)
                        category['value']['max'].append(max_expectation)
                        category['importance'].append(importance)
                        criteria_order.remove(criteria_num)
                    except:
                        pass
                # product specs
                index = raw.index('\nSurvey') + 1
                while index < len(raw) and not raw[index] == PAGE_TERMINATOR:
                    index, product_name = get_next_str(raw, index)
                    company_name = COMPANY_PRODUCT_MAP[product_name[0:1]]
                    company_data = COMPANIES[company_name]
                    product_data = company_data['products'][product_name]
                    segment_analysis = product_data['segment_analysis']
                    for category in segment_analysis.keys():
                        index, value = get_next_val(raw, index)
                        if not value == -1:
                            segment_analysis[category].append(value)
                # next page
                page_number += 1
            # market share page
            viewer.navigate(10)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index('100.0%', raw.index('100.0%') + 1) + 1
            #print('> market share')
            # HR/TQM report
            viewer.navigate(12)
            viewer.render()
            raw = viewer.canvas.strings
            # HR section
            #print('> HR report')
            index = raw.index(' Needed Complement')
            # TQM section
            #print('> TQM report')
            index = raw.index(' CPI Systems')
        file_count = file_count + 1
    if file_count < 2:
        print('Program needs at least 2 rounds to perform analysis')
        exit()
    return round_numbers, round_years

def load_file(file_path : str):
    global ANNUAL_REPORT
    global COMPANIES
    global MARKET_SEGMENTS
    json_data : dict = None
    with open(file_path, 'rb') as file:
        json_data = json.loads(file.read())
    keys_exist = lambda *keys: False not in list(map(lambda key: key.lower() in json_data.keys(), keys))
    if not keys_exist('round_years', 'round_numbers', 'company_data', 'market_data', 'annual_report'):
        print('not a valid json export file')
        exit()
    def parse_table(json_table : dict, obj_table : dict):
        for key in json_table.keys():
            if not key in obj_table.keys():
                if type(json_table[key]) is dict:
                    obj_table[key] = { }
                elif type(json_table[key]) is list:
                    obj_table[key] = [ ]
            if type(json_table[key]) is dict:
                parse_table(json_table[key], obj_table[key])
            elif type(json_table[key]) is list:
                obj_table[key].extend(json_table[key])
            else:
                obj_table[key] = json_table[key]
    parse_table(json_data['annual_report'], ANNUAL_REPORT)
    parse_table(json_data['company_data'], COMPANIES)
    parse_table(json_data['market_data'], MARKET_SEGMENTS)
    round_years : list = json_data['round_years']
    round_numbers : list = json_data['round_numbers']
    print('Loading data for Rounds {0}, Years {1}'.format(round_numbers, round_years))
    return round_numbers, round_years

def main(round_numbers : list, round_years : list):
    commands : dict = None
    # commands
    # command_help: lists available commands
    def command_help(cmd_name : str = None, vargs : any = None):
        if not cmd_name is None and cmd_name.lower() in commands.keys():
            print('{0}\t\t:\t{1}'.format(cmd_name, commands[cmd_name]['desc']))
            if 'args' in commands[cmd_name].keys():
                print('\t{0}'.format(commands[cmd_name]['args']))
        else:
            for cmd_name in sorted(commands.keys()):
                print('{0}\t\t:\t{1}'.format(cmd_name, commands[cmd_name]['desc']))
        return 0
    # command_test: prints the word 'test'
    def command_test(arg : any = None, vargs : any = None):
        print('test')
        return 0
    # command_exit: safely exits program w/o keyboard interrupt (CTRL+C)
    def command_exit(arg : any = None, vargs : any = None):
        return exit()
    # command_product: displays information on products
    def command_product(context_choice : str = None, proc_args : tuple = (None, None)):
        def context_segment(segment_choice : str = None):
            segment_list : list[str] = [segment.lower() for segment in MARKET_SEGMENTS.keys()]
            if segment_choice is None:
                print('please choose a market segment:')
                for market_segment in segment_list:
                    print('* {0}'.format(market_segment))
                print('or enter "back" to choose a context')
                while segment_choice is None:
                    user_choice = input('>>>product> ').lower()
                    if user_choice == 'back':
                        return command_product('segment')
                    elif user_choice in segment_list:
                        segment_choice = user_choice
                    else:
                        print('not a valid segment choice. try again')
            # capitalize the first letter
            segment_choice = segment_choice.capitalize()
            display_trends : bool = None
            if max(round_numbers) < MAX_NUM_ROUNDS:
                print('would you like to graph trend lines for future rounds? (y/n)')
                while display_trends is None:
                    user_choice = input('>>>product> ').lower()
                    # "yes or no" but anything other than an explicit yes is a no
                    # this is a good rule for life in general
                    if user_choice[0] == 'y':
                        display_trends = True
                    else:
                        display_trends = False
            else:
                # if we've reached the final round, no reason to display trends
                display_trends = False
            product_fields : list = [ ]
            for category_name in PRODUCT_INFO.keys():
                category_data = PRODUCT_INFO[category_name]
                if type(category_data) is dict:
                    product_fields.append(PyInquirer.Separator('=== {0} ==='.format(category_name)))
                    for field_name in category_data.keys():
                        product_fields.append({
                            'name': field_name,
                            'value': '{0}/{1}'.format(category_name, field_name)
                        })
            validate_fields = lambda chosen_fields: 'must choose at least one field to examine' if len(chosen_fields) < 1 else True
            chosen_fields = PyInquirer.prompt([
                {
                    'type': 'checkbox',
                    'message': 'Select product fields to display',
                    'name': 'product_fields',
                    'choices': product_fields,
                    'validate': validate_fields
                }
            ], style = CONSOLE_STYLE)
            graph : dict[dict] = { }
            for chosen_field in chosen_fields['product_fields']:
                [category_name, field_name] = chosen_field.split('/')
                for company_name in COMPANIES:
                    company_products = COMPANIES[company_name]['products']
                    for product_key in company_products.keys():
                        product_data = company_products[product_key]
                        if product_data['primary_segment'] == segment_choice:
                            product_name = product_data['product_name']
                            if not chosen_field in graph.keys():
                                graph[chosen_field] = { }
                            field_data = product_data[category_name][field_name]
                            graph[chosen_field][product_name] = field_data
            pyplot_settings : dict = None
            with open('pyplot.json', 'rb') as file:
                pyplot_settings = json.loads(file.read())
            x_label, x_data_base = 'round #', round_numbers
            x_data_origin_size = len(x_data_base)
            pyplot.figure()
            num_fields : int = len(graph.keys())
            graph_ncols : int = math.ceil(num_fields / 2)
            graph_nrows : int = math.floor(num_fields / 2)
            for field_name in graph.keys():
                field_data = graph[field_name]
                plot_handles : list = [ ]
                plot_labels : list = [ ]
                y_min : float = 2147483647.0
                y_max : float = -2147483647.0
                field_index : int = list(key for key in graph.keys()).index(field_name)
                pyplot.subplot(graph_nrows, graph_ncols, 1 + field_index)
                for product_name in field_data.keys():
                    # graph data
                    plot_labels.append(product_name)
                    x_data : list = x_data_base.copy()
                    y_data : list = field_data[product_name]
                    # visual data
                    company_name : str = COMPANY_PRODUCT_MAP[product_name[0:1]]
                    plot_settings : dict = pyplot_settings[company_name]
                    plot_color : str = plot_settings['color']
                    plot_marker : str = plot_settings['marker']
                    # calculate trend data
                    if display_trends is True:
                        try:
                            trend = numpy.poly1d(numpy.polyfit(x_data, y_data, 1))
                            x_data.append(x_data[-1] + 1)
                            y_data.append(trend(len(x_data)))
                        except:
                            print('failed to trend data')
                            print('x: {0}\r\ny:{1}'.format(x_data, y_data))
                            return 0
                    # plot data w/ visual effects
                    try:
                        product_plot, = pyplot.plot(x_data, y_data, color=plot_color, 
                            linestyle='solid', marker=plot_marker, linewidth=1, markersize=6)
                        plot_handles.append(product_plot)
                        y_min = min(y_min, min(y_data))
                        y_max = max(y_max, max(y_data))
                    except:
                        print('failed to plot data')
                        print('x: {0}\r\ny:{1}'.format(x_data, y_data))
                        return 0
                y_padding = math.abs(y_max - y_min) * 0.1
                y_min = y_min - y_padding
                y_max = y_max + y_padding
                pyplot.legend(handles=plot_handles, labels=plot_labels, fontsize='x-small', loc='best', ncol=2)
                pyplot.title('segment: {0}\n{1}'.format(segment_choice, field_name))
                pyplot.xticks(x_data, list(map(lambda tick: str(tick), x_data)))
                pyplot.xlim(xmin=1, xmax=max(x_data))
                pyplot.ylim(ymin=y_min, ymax=y_max)
                if display_trends is True:
                    pyplot.vlines(x=x_data[x_data_origin_size - 1], linestyle='dashdot', \
                        ymin=y_min, ymax=y_max, colors='black')
                pyplot.xlabel(x_label)
                pyplot.grid(True)
            pyplot.tight_layout()
            pyplot.show()
        def context_teams():
            pass
        analyze_context : dict = {
            'segment': {
                'desc': 'view products per segment',
                'proc': context_segment
            },
            'teams': {
                'desc': 'view products per team(s)',
                'proc': context_teams
            }
        }
        if context_choice is None:
            print('please choose which context to analyze a product(s) in')
            for context_name in analyze_context.keys():
                print('* {0} : {1}'.format(context_name, analyze_context[context_name]['desc']))
            print('or enter "menu" to return to the menu')
            while context_choice is None:
                user_choice = input('>>>product> ').lower()
                if user_choice == 'menu':
                    return -1
                elif user_choice in analyze_context.keys():
                    context_choice = user_choice
                else:
                    print('not a valid context choice. try again')
        context_proc = analyze_context[context_choice]['proc']
        if type(proc_args) is tuple and len(proc_args) > 0:
            context_proc(*proc_args)
        else:
            context_proc()
        return 0
    def print_intro():
        print('Welcome to the Capxamin menu')
        print('Author: John Carr <jxc9224@rit.edu>')
        print('Github: https://github.com/jxc9224/capxamin')
        print('Enter a command to get started, or "help" to list available commands\r\n')
    def command_clear(arg : any = None, vargs : any = None):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear')
        print_intro()
        return 0
    def command_export(file_path : any = None, vargs : any = None):
        if file_path is None:
            print('please enter a valid file name')
            return 0
        if not file_path[len(JSON_EXT)*-1:] == JSON_EXT:
            file_path = file_path + JSON_EXT
        with open(file_path, 'a') as file:
            file.write(json.dumps({
                'round_years': round_years,
                'round_numbers': round_numbers,
                'company_data': COMPANIES, 
                'market_data': MARKET_SEGMENTS, 
                'annual_report': ANNUAL_REPORT
            }))
            print('\r\nsaved to: {0}'.format(os.path.realpath(file.name)))
        return 0
    commands = {
        'clear': {
            'desc': 'clears console screen',
            'proc': command_clear
        },
        'export': {
            'args': 'export [file_name]',
            'desc': 'exports all collected info to a json file',
            'proc': command_export
        },
        'product': {
            'args': 'product [segment [trad|low|high|pfmn|size] | teams *[a|b|c|d|e|f]]',
            'desc': 'display product fields in a given context (segment, teams, ...)',
            'proc': command_product
        },
        'help': {
            'args': 'help [command_name]',
            'desc': 'lists available commands',
            'proc': command_help
        },
        'test': {
            'desc': 'prints the word "test"',
            'proc': command_test
        },
        'exit': {
            'desc': 'exits program',
            'proc': command_exit
        }
    }
    # enter main program loop
    print_intro()
    user_input : str = None
    while True:
        user_input = input('>>> ').lower().strip()
        command = user_input.split(' ')
        command_name = command[0]
        if command_name in commands.keys():
            proc = commands[command_name]['proc']
            proc_arg = len(command) > 1 and command[1] or None
            proc_vargs = len(command) > 2 and tuple(command[2:]) or None
            proc_result : int = proc(proc_arg, proc_vargs)
            # if proc_result = -1, user chose to return to menu
            if proc_result == -1:
                print_intro()
            else:
                print('\r\n')
        elif command_name == '':
            pass
        else:
            print('Not a valid command. Use "help" to list available commands')

if __name__ == '__main__':
    # load input directory or json file
    round_years : list = None
    round_numbers : list = None
    input_path : str = sys.argv[1]
    if os.path.isdir(input_path):
        round_numbers, round_years = load_folder(input_path)
    elif os.path.isfile(input_path) and IS_FILE_EXT(input_path, '.json'):
        round_numbers, round_years = load_file(input_path)
    else:
        print('no valid input provided. please input a folder path or json file')
        exit()
    # enter main loop
    main(round_numbers, round_years)
