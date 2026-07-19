import pandas as pd
import random
from datetime import datetime, timedelta

# 1. Định nghĩa các danh mục dữ liệu thực tế trong ngành Freight Forwarding
CARRIERS = ['Maersk', 'MSC', 'CMA CGM', 'COSCO', 'ONE', 'Evergreen', 'Hapag-Lloyd']
POLS = ['VNHPH (Hai Phong)', 'VNSGN (Cat Lai)', 'VNDNG (Da Nang)']
PODS = ['USLAX (Los Angeles)', 'USLGB (Long Beach)', 'NLRTM (Rotterdam)', 'DEHAM (Hamburg)', 'CNSHA (Shanghai)']
CONTAINER_TYPES = ['20DC', '40HC']
CURRENCIES = ['USD']

def generate_freight_data(num_records=1000):
    data = []
    base_date = datetime.now()
    
    for i in range(1, num_records + 1):
        carrier = random.choice(CARRIERS)
        pol = random.choice(POLS)
        pod = random.choice(PODS)
        container_type = random.choice(CONTAINER_TYPES)
        
        # Giả lập logic cước: Container 40HC đắt hơn 20DC, đi Châu Mỹ (US) đắt hơn Châu Á (CN)
        if 'US' in pod:
            base_rate = random.randint(2500, 4000) if container_type == '40HC' else random.randint(1800, 2800)
        elif 'NL' in pod or 'DE' in pod:
            base_rate = random.randint(2000, 3200) if container_type == '40HC' else random.randint(1400, 2200)
        else:
            base_rate = random.randint(400, 800) if container_type == '40HC' else random.randint(200, 500)
            
        # Giả lập các khoản phụ phí Local Charges (THC, Seal, Doc)
        thc_fee = 140 if container_type == '20DC' else 210
        seal_fee = 10
        doc_fee = 40
        
        # Ngày hiệu lực cước (Validity)
        valid_from = base_date + timedelta(days=random.randint(-15, 15))
        valid_to = valid_from + timedelta(days=15)
        
        row = {
            "Rate_ID": f"RTE-{i:05d}",
            "Carrier": carrier,
            "POL_Origin": pol,
            "POD_Destination": pod,
            "Container_Type": container_type,
            "Ocean_Freight_USD": base_rate,
            "THC_USD": thc_fee,
            "Seal_Fee_USD": seal_fee,
            "Doc_Fee_USD": doc_fee,
            "Total_Cost_USD": base_rate + thc_fee + seal_fee + doc_fee,
            "Valid_From": valid_from.strftime('%Y-%m-%d'),
            "Valid_To": valid_to.strftime('%Y-%m-%d'),
            "Transit_Time_Days": random.randint(12, 35)
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    return df

# Run & Export ra file CSV
df_synthetic = generate_freight_data(1000)
df_synthetic.to_csv('synthetic_freight_rates.csv', index=False)
print("Đã tạo thành công 1,000 dòng dữ liệu cước tại file 'synthetic_freight_rates.csv'!")