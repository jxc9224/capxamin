import datetime, os, sys
import numpy, numpy.typing, pdfreader
import matplotlib.pyplot as pyplot

CAPSIM_START_YEAR : int = 2022
CAPSIM_GAME_ID : str = 'C133749'
CAPSIM_TEAM_NAME : str = 'Andrews'

SEGMENT_INFO = {
    'total_industry_unit_demand': numpy.array([], dtype=int),
    'actual_industry_unit_sales': numpy.array([], dtype=int),
    'segment_percent_of_total_industry': numpy.array([], dtype=float),
    'next_year_segment_growth_rate': numpy.array([], dtype=float),

    'customer_buying_criteria': {
        'ideal_age': {
            'value': numpy.array([], dtype=float),
            'importance': numpy.array([], dtype=float)
        },
        'price': {
            'value': {
                'min': numpy.array([], dtype=float),
                'max': numpy.array([], dtype=float)
            },
            'importance': numpy.array([], dtype=float)
        },
        'ideal_position': {
            'value': {
                'pfmn': numpy.array([], dtype=float),
                'size': numpy.array([], dtype=float)
            },
            'importance': numpy.array([], dtype=float)
        },
        'mtbf': {
            'value': {
                'min': numpy.array([], dtype=int),
                'max': numpy.array([], dtype=int)
            },
            'importance': numpy.array([], dtype=float)
        },
    }
}

MARKET_SEGMENTS = { 
    'Trad': SEGMENT_INFO.copy(), 
    'Low': SEGMENT_INFO.copy(), 
    'High': SEGMENT_INFO.copy(), 
    'Pfmn': SEGMENT_INFO.copy(), 
    'Size': SEGMENT_INFO.copy() 
}

PRODUCT_INFO = {
    'product_name': '{product_name}',
    'primary_segment': '{primary_segment}',

    'production_analysis': {
        'units_sold': numpy.array([], dtype=float),
        'unit_inventory': numpy.array([], dtype=float),
        'revision_date': numpy.array([], dtype=datetime.datetime),
        'age_dec_31': numpy.array([], dtype=float),
        'mtbf': numpy.array([], dtype=float),
        'pfmn_coord': numpy.array([], dtype=float),
        'size_coord': numpy.array([], dtype=float),
        'price': numpy.array([], dtype=float),
        'material_cost': numpy.array([], dtype=float),
        'labor_cost': numpy.array([], dtype=float),
        'contribution_margin': numpy.array([], dtype=float),
        '2nd_shift_and_overtime': numpy.array([], dtype=float),
        'automation_next_round': numpy.array([], dtype=float),
        'capacity_next_round': numpy.array([], dtype=float),
        'plant_utilization': numpy.array([], dtype=float)
    },

    'segment_analysis': {
        'market_share': numpy.array([], dtype=float),
        'units_sold_to_seg': numpy.array([], dtype=float),
        'revision_date': numpy.array([], dtype=datetime.datetime),
        #'stock_out': numpy.array([], dtype=bool), # TODO: something for this? lol
        'pfmn_coord': numpy.array([], dtype=float),
        'size_coord': numpy.array([], dtype=float),
        'list_price': numpy.array([], dtype=float),
        'mtbf': numpy.array([], dtype=float),
        'age_dec_31': numpy.array([], dtype=float),
        'promo_budget': numpy.array([], dtype=float),
        'customer_awareness': numpy.array([], dtype=float),
        'sales_budget': numpy.array([], dtype=float),
        'customer_accessibility': numpy.array([], dtype=float),
        'customer_survery_score': numpy.array([], dtype=float)
    },

    'market_share': {
        'actual': {
            'trad': numpy.array([], dtype=float),
            'low': numpy.array([], dtype=float),
            'high': numpy.array([], dtype=float),
            'pfmn': numpy.array([], dtype=float),
            'size': numpy.array([], dtype=float),
            'total': numpy.array([], dtype=float)
        },
        'potential': {
            'trad': numpy.array([], dtype=float),
            'low': numpy.array([], dtype=float),
            'high': numpy.array([], dtype=float),
            'pfmn': numpy.array([], dtype=float),
            'size': numpy.array([], dtype=float),
            'total': numpy.array([], dtype=float)
        },
    }
}

COMPANY_INFO = {
    'selected_financial_stats': {
        'return_on_sales': numpy.array([], dtype=float),
        'asset_turnover': numpy.array([], dtype=float),
        'return_on_assets': numpy.array([], dtype=float),
        'leverage': numpy.array([], dtype=float),
        'return_on_equity': numpy.array([], dtype=float),
        'emergency_loan': numpy.array([], dtype=float),
        'sales': numpy.array([], dtype=float),
        'ebit': numpy.array([], dtype=float),
        'profits': numpy.array([], dtype=float),
        'cumulative_profit': numpy.array([], dtype=float),
        'sga_sales': numpy.array([], dtype=float),
        'contribution_margin': numpy.array([], dtype=float)
    },
    'stock': {
        'close': numpy.array([], dtype=float),
        'change': numpy.array([], dtype=float),
        'shares': numpy.array([], dtype=int),
        'market_cap': numpy.array([], dtype=float),
        'book_value_per_share': numpy.array([], dtype=float),
        'earnings_per_share': numpy.array([], dtype=float),
        'dividend': numpy.array([], dtype=float),
        'yield_percent': numpy.array([], dtype=float),
        'price_to_earnings': numpy.array([], dtype=float)
    },
    'products': {
        # filled in when analyzing production analysis
        # 'product_name': copy(PRODUCT_INFO),
    },
    'financial': {
        'net_income': numpy.array([], dtype=float),
        'adj_depreciation': numpy.array([], dtype=float),
        'adj_extraordinary': numpy.array([], dtype=float),
        'changes_accounts_payable': numpy.array([], dtype=float),
        'changes_accounts_receivable': numpy.array([], dtype=float),
        'changes_inventory': numpy.array([], dtype=float),
        'net_cash_operations': numpy.array([], dtype=float),
        'plant_improvements': numpy.array([], dtype=float),
        'dividends_paid': numpy.array([], dtype=float),
        'sales_common_stock': numpy.array([], dtype=float),
        'purchase_common_stock': numpy.array([], dtype=float),
        'long_term_debt_issued': numpy.array([], dtype=float),
        'long_term_debt_early_retire': numpy.array([], dtype=float),
        'current_debt_retirement': numpy.array([], dtype=float),
        'current_debt_borrowing': numpy.array([], dtype=float),
        'emergency_loan_paid': numpy.array([], dtype=float),
        'net_cash_financing': numpy.array([], dtype=float),
        'net_change_cash_position': numpy.array([], dtype=float),
        'cash': numpy.array([], dtype=float),
        'accounts_receivable': numpy.array([], dtype=float),
        'inventory': numpy.array([], dtype=float),
        'total_current_assets': numpy.array([], dtype=float),
        'plant_and_equipment': numpy.array([], dtype=float),
        'accumulated_depreciation': numpy.array([], dtype=float),
        'total_fixed_assets': numpy.array([], dtype=float),
        'total_assets': numpy.array([], dtype=float),
        'accounts_payable': numpy.array([], dtype=float),
        'current_debt': numpy.array([], dtype=float),
        'total_current_liabilities': numpy.array([], dtype=float),
        'long_term_debt': numpy.array([], dtype=float),
        'total_liabilities': numpy.array([], dtype=float),
        'common_stock': numpy.array([], dtype=float),
        'retained_earnings': numpy.array([], dtype=float),
        'total_equity': numpy.array([], dtype=float),
        'total_liabilities_and_owners_equity': numpy.array([], dtype=float),
        'sales': numpy.array([], dtype=float),
        'variable_costs': numpy.array([], dtype=float),
        'contribution_margin': numpy.array([], dtype=float),
        'depreciation': numpy.array([], dtype=float),
        'sga': numpy.array([], dtype=float),
        'other': numpy.array([], dtype=float),
        'ebit': numpy.array([], dtype=float),
        'interest': numpy.array([], dtype=float),
        'taxes': numpy.array([], dtype=float),
        'profit_sharing': numpy.array([], dtype=float),
        'net_profit': numpy.array([], dtype=float)
    },
    'human_resources': {

    },
    'tqm': {
        'cpi_systems': numpy.array([], dtype=float),
        'vendorjit': numpy.array([], dtype=float),
        'quality_initiative_training': numpy.array([], dtype=float),
        'channel_support_systems': numpy.array([], dtype=float),
        'concurrent_engineering': numpy.array([], dtype=float),
        'unep_green_programs': numpy.array([], dtype=float),
        
        'benchmarking': numpy.array([], dtype=float),
        'quality_function_deployment_effort': numpy.array([], dtype=float),
        'cce6_sigma_training': numpy.array([], dtype=float),
        'gemi_tqem': numpy.array([], dtype=float),
        'total_expenditures': numpy.array([], dtype=float),
        
        'material_cost_reduction': numpy.array([], dtype=float),
        'labor_cost_reduction': numpy.array([], dtype=float),
        'reduction_rd_cycle_time': numpy.array([], dtype=float),
        'reduction_admin_costs': numpy.array([], dtype=float),
        'demand_increase': numpy.array([], dtype=float)
    }
}

COMPANIES = {
    'Andrews': COMPANY_INFO.copy(),
    'Baldwin': COMPANY_INFO.copy(),
    'Chester': COMPANY_INFO.copy(),
    'Digby': COMPANY_INFO.copy(),
    'Erie': COMPANY_INFO.copy(),
    'Ferris': COMPANY_INFO.copy()
}

COMPANY_PRODUCT_MAP = {
    'A': 'Andrews',
    'B': 'Baldwin',
    'C': 'Chester',
    'D': 'Digby',
    'E': 'Erie',
    'F': 'Ferris'
}

INCOME_STATEMENT_ITEM = {
    'sales': numpy.array([], dtype=float),
    'direct_labor': numpy.array([], dtype=float),
    'direct_material': numpy.array([], dtype=float),
    'inventory_carry': numpy.array([], dtype=float),
    'total_variable_costs': numpy.array([], dtype=float),
    'contribution_margin': numpy.array([], dtype=float),
    'depreciation': numpy.array([], dtype=float),
    'sga_rnd': numpy.array([], dtype=float),
    'sga_rnd_promotions': numpy.array([], dtype=float),
    'sga_rnd_sales': numpy.array([], dtype=float),
    'sga_rnd_admin': numpy.array([], dtype=float),
    'total_period_costs': numpy.array([], dtype=float),
    'net_margin': numpy.array([], dtype=float),
    # the following are only used by summary items
    'other': numpy.array([], dtype=float),
    'ebit': numpy.array([], dtype=float),
    'short_term_interest': numpy.array([], dtype=float),
    'long_term_interest': numpy.array([], dtype=float),
    'taxes': numpy.array([], dtype=float),
    'profit_sharing': numpy.array([], dtype=float),
    'net_profit': numpy.array([], dtype=float)
}

ANNUAL_REPORT = {
    'income_statement': {
        # your teams products are copied here
        # 'product_name': copy(INCOME_STATEMENT_ITEM)
        # along with the following summary items
        'year_total': INCOME_STATEMENT_ITEM.copy(),
        'common_size': INCOME_STATEMENT_ITEM.copy()
    }
}

NULL_STR = 'n/a'
DATE_FORMAT : str = '%m/%d/%Y'
PAGE_TERMINATOR : str = 'CAPSTONE ® COURIER'

def get_next_str(raw : list, start : int):
    for index in range(start, len(raw)):
        if raw[index] in COMPANIES.keys():
            # company names
            return index + 1, raw[index]
        elif len(raw[index]) >= 3 and raw[index][0:1] in [ 'A', 'B', 'C', 'D', 'E', 'F' ]:
            # product names
            return index + 1, raw[index]
            # product segments
        elif raw[index] in MARKET_SEGMENTS.keys():
            return index + 1, raw[index]
    return start + 1, NULL_STR

def get_next_val(raw : list, start : int):
    for index in range(start, len(raw)):
        if raw[index][-1:] == '%':
            # percent value
            return index + 1, float(raw[index][0:-1]) / 100
        elif raw[index][0] == '(':
            # negative dollar value
            return index + 1, -1 * float('0' + raw[index].replace(',', '')[2:-1])
        elif raw[index][0] == '$':
            # positive dollar value
            return index + 1, float('0' + raw[index].replace(',', '')[1:])
        else:
            # datetime value
            try:
                return index + 1, datetime.datetime.strptime(raw[index], DATE_FORMAT).strftime(DATE_FORMAT)
            except:
                # base case: float/int value
                # if it's not this then it's nothing useful
                try:
                    value = raw[index].replace(',', '')
                    return index + 1, '.' in value and float(value) or int(value)
                except:
                    pass
    return start + 1, -1

def main(folder_path : str):
    # step 1: collect & organize
    raw : list = None
    index : int = None 
    value : int | float | datetime.datetime = None
    viewer : pdfreader.SimplePDFViewer = None
    # start scan on input directory
    for pdf_file_path in os.scandir(folder_path):
        print('Reading: {0}'.format(pdf_file_path))
        # open next capstone courier pdf file
        with open(pdf_file_path, 'rb') as file:
            company_name : str = NULL_STR
            company_data : dict = None
            # create pdf viewer object for courier file
            viewer = pdfreader.SimplePDFViewer(file)
            # selected financial stats page
            viewer.navigate(1)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index(' ROS') + 1
            #print('> selected financial stats')
            for category in COMPANY_INFO['selected_financial_stats'].keys():
                for company_name in COMPANIES.keys():
                    company_data = COMPANIES[company_name]
                    index, value = get_next_val(raw, index)
                    numpy.append(company_data['selected_financial_stats'][category], value)
                    #print(company_name, category, value)
                index += 1
            # stock market summary page
            viewer.navigate(2)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index('P/E') + 1
            #print('> stock summary')
            for company_name in COMPANIES.keys():
                index = raw.index(company_name)
                company_data = COMPANIES[company_name]
                for category in company_data['stock'].keys():
                    index, value = get_next_val(raw, index)
                    if not value == -1:
                        numpy.append(company_data['stock'][category], value)
                        #print(company_name, category, value)
            # financial summary page
            viewer.navigate(3)
            viewer.render()
            raw = viewer.canvas.strings
            index = raw.index(' Net Income(Loss)') + 1
            #print('> finance summary')
            for category in COMPANY_INFO['financial'].keys():
                for company_name in COMPANIES.keys():
                    company_data = COMPANIES[company_name]
                    index, value = get_next_val(raw, index)
                    if not value == -1:
                        numpy.append(company_data['financial'][category], value)
                        #print(company_name, category, value)
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
                index, primary_seg = get_next_str(raw, index)
                company_name = COMPANY_PRODUCT_MAP[product_name[0:1]]
                company_data = COMPANIES[company_name]
                product_data = PRODUCT_INFO.copy()
                product_data['product_name'] = product_name
                product_data['primary_segment'] = primary_seg
                company_data['products'][product_name] = product_data
                for category in PRODUCT_INFO['production_analysis'].keys():
                    index, value = get_next_val(raw, index)
                    if not value == -1:
                        numpy.append(product_data['production_analysis'][category], value)
                        #print(company_name, product_name, category, value)
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
                numpy.append(market_seg_data['total_industry_unit_demand'], value)
                #print(market_segment, 'total_industry_unit_demand', value)
                index = raw.index(' Actual Industry Unit Sales') + 1
                value = int(raw[index].replace(',', '').replace('|', ''))
                numpy.append(market_seg_data['actual_industry_unit_sales'], value)
                #print(market_segment, 'actual_industry_unit_sales', value)
                index = raw.index(' Segment % of Total Industry') + 1
                value = float(raw[index][0:-1].replace(',', '').replace('|', '')) / 100
                numpy.append(market_seg_data['segment_percent_of_total_industry'], value)
                #print(market_segment, 'segment_percent_of_total_industry', value)
                index = raw.index("Next Year's Segment Growth Rate") + 1
                value = float(raw[index][0:-1].replace(',', '').replace('|', '')) / 100
                numpy.append(market_seg_data['next_year_segment_growth_rate'], value)
                #print(market_segment, 'next_year_segment_growth_rate', value)
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
                        numpy.append(category['value'], expectation)
                        numpy.append(category['importance'], importance)
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
                        numpy.append(category['value']['min'], min_expectation)
                        numpy.append(category['value']['max'], max_expectation)
                        numpy.append(category['importance'], importance)
                        criteria_order.remove(criteria_num)
                        #print(market_segment, criteria_num + '. Price', min_expectation, max_expectation, importance)
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
                        numpy.append(category['value']['pfmn'], pfmn_expectation)
                        numpy.append(category['value']['size'], size_expectation)
                        numpy.append(category['importance'], importance)
                        criteria_order.remove(criteria_num)
                        #print(market_segment, criteria_num + '. Ideal Position', pfmn_expectation, size_expectation, importance)
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
                        numpy.append(category['value']['min'], min_expectation)
                        numpy.append(category['value']['max'], max_expectation)
                        numpy.append(category['importance'], importance)
                        criteria_order.remove(criteria_num)
                        #print(market_segment, criteria_num + '. Reliability', min_expectation, max_expectation, importance)
                    except:
                        pass
                # product specs
                index = raw.index('\nSurvey') + 1
                while index < len(raw) and not raw[index] == PAGE_TERMINATOR:
                    index, product_name = get_next_str(raw, index)
                    company_name = COMPANY_PRODUCT_MAP[product_name[0:1]]
                    company_data = COMPANIES[company_name]
                    product_data = company_data['products'][product_name]
                    for category in PRODUCT_INFO['segment_analysis'].keys():
                        index, value = get_next_val(raw, index)
                        if not value == -1:
                            numpy.append(product_data['segment_analysis'][category], value)
                            #print(market_segment, company_name, product_name, category, value)
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
    # step 2: process
    running : bool = True
    user_input : str = None
    print('Welcome to CapCoAnalyze')
    print('Enter a command to get started, or "help" to list available commands')
    commands : dict = None
    commands = {
        'help': {
            'desc': 'lists available commands',
            'proc': (lambda : (
                for cmd in commands.keys():
                    print(cmd + ' : ' + commands[cmd]['desc'])
            ))
        },
        'test': {
            'desc': 'prints the word "test"'
            'proc': (lambda: (
                print('test')
            ))
        }
    }
    while running = True:
        user_input = input('> ').lower()
        if user_input in commands.keys():
            cmd : dict = commands[user_input]
            proc = cmd['proc']
            proc()
        else:
            print('Not a valid command. Use "help" to list available commands')

if __name__ == '__main__':
    main(sys.argv[1])
