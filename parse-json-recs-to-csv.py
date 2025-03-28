import json
import csv
import datetime
import sys

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E'}
    while size > power:
        size /= power
        n += 1
    return '%.1f' % size + power_labels[n] + 'B'

def format_gb(size):
    return '%.12f' % (size / 1024 / 1024 / 1024)

def format_query_frequency(qf):
    if qf == 0.0:
        return 'never'
    elif qf < 1.0:
        return 'rarely'
    elif qf <= 40.0:
        return 'sometimes'
    elif qf <= 90.0:
        return 'often'
    else:
        return 'always'

# Check if the JSON file name is provided as an argument
if len(sys.argv) != 3:
    print("Usage: python3 parse-json-recs-to-csv.py <json_file> <price_per_gb>")
    sys.exit(1)

price_per_gb = float(sys.argv[2])
json_file_name = sys.argv[1]
csv_file_name = json_file_name.replace('.json', '.csv')

with open(json_file_name, 'r') as json_file:
    data = json.load(json_file)

with open(csv_file_name, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['As of Date', 'Pattern', 'Total Volume', 'Recommended Drop Rate', 'service_name', 'App Code', 'Merchandizing App Code', 'Query Frequency', 'service_volume', 'formatted_service_volume', 'service_count', 'Estimated Drop Volume', 'Formatted Estimated Drop Volume', 'Formatted Estimated Drop Volume in GB', 'Estimated Savings ($0.24/GB)'])

    for item in data:
        pattern = item['pattern']
        volume = item['volume']
        recommended_drop_rate = item['recommended_drop_rate']
        attribution = item.get('attribution', {})
        today = datetime.datetime.now().strftime("%m/%d/%Y")
        query_frequency = 100.0 * item['queried_lines'] / item['ingested_lines']

        for service_name, service_data in attribution.items():
            current_service_name = service_name.split('=', 1)[1].strip('"}')
            app_code = current_service_name.split('-', 1)[0]
            is_merchandizing_app_code = ''
            if current_service_name.upper().startswith('OMS'):
                is_merchandizing_app_code = 'OMS'
            elif current_service_name.upper().startswith('OCPE'):
                is_merchandizing_app_code = 'OCPE'
            elif current_service_name.upper().startswith('OCPS'):
                is_merchandizing_app_code = 'OCPS'
            elif current_service_name.upper().startswith('OCRP'):
                is_merchandizing_app_code = 'OCRP'
            elif current_service_name.upper().startswith('OCOM'):
                is_merchandizing_app_code = 'OCOM'
            elif current_service_name.upper().startswith('MEVIR'):
                is_merchandizing_app_code = 'MEVIR'
            elif current_service_name.upper().startswith('MEITEM'):
                is_merchandizing_app_code = 'MEITEM'
            elif current_service_name.upper().startswith('MEBP'):
                is_merchandizing_app_code = 'MEBP'
            elif current_service_name.upper().startswith('MEUPP'):
                is_merchandizing_app_code = 'MEUPP'
            elif current_service_name.upper().startswith('MECOST'):
                is_merchandizing_app_code = 'MECOST'
            elif current_service_name.upper().startswith('MEVEND'):
                is_merchandizing_app_code = 'MEVEND'
            elif current_service_name.upper().startswith('MEMSP'):
                is_merchandizing_app_code = 'MEMSP'
            elif current_service_name.upper().startswith('APEX'):
                is_merchandizing_app_code = 'APEX'
            elif current_service_name.upper().startswith('PPAP'):
                is_merchandizing_app_code = 'PPAP'
            else:
                is_merchandizing_app_code = ''
            writer.writerow([
                today,
                pattern,
                volume,
                recommended_drop_rate,
                current_service_name,
                app_code,
                is_merchandizing_app_code,
                format_query_frequency(query_frequency),
                service_data['Volume'],
                format_bytes(service_data['Volume']),
                service_data['Count'],
                recommended_drop_rate / 100.0 * service_data['Volume'],
                format_bytes(recommended_drop_rate / 100.0 * service_data['Volume']),
                format_gb(recommended_drop_rate / 100.0 * service_data['Volume']),
                price_per_gb * float(format_gb(recommended_drop_rate / 100.0 * service_data['Volume']))
            ])
