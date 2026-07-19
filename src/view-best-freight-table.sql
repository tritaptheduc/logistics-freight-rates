-- Tạo hoặc thay thế View có tên là vw_best_freight_rates trong Dataset freight_database
CREATE OR REPLACE VIEW `freight-analytics-project.freight_database.vw_best_freight_rates` AS

WITH RankedRates AS (
    SELECT 
        Rate_ID,
        Carrier,
        POL_Origin,
        POD_Destination,
        Container_Type,
        Ocean_Freight_USD,
        THC_USD,
        Seal_Fee_USD,
        Doc_Fee_USD,
        Total_Cost_USD,
        
        -- 1. Tính toán giá chào bán cho khách hàng (Margin 15%)
        ROUND(Total_Cost_USD * 1.15, 2) AS Quoted_Price_USD,
        
        -- 2. Tính lợi nhuận dự kiến trên mỗi container (USD)
        ROUND(Total_Cost_USD * 0.15, 2) AS Expected_Profit_USD,
        
        Valid_From,
        Valid_To,
        Transit_Time_Days,
        
        -- 3. Kiểm tra trạng thái cước (Còn hiệu lực hay Hết hạn)
        CASE 
            WHEN CURRENT_DATE() BETWEEN Valid_From AND Valid_To THEN 'Active'
            ELSE 'Expired'
        END AS Rate_Status,

        -- 4. Đánh số thứ tự giá cước từ thấp đến cao cho từng Tuyến đường & Loại cont
        ROW_NUMBER() OVER(
            PARTITION BY POL_Origin, POD_Destination, Container_Type 
            ORDER BY Total_Cost_USD ASC, Transit_Time_Days ASC
        ) AS rate_rank

    FROM 
        `freight-analytics-project.freight_database.raw_freight_rates`
)

-- Chỉ giữ lại hãng tàu có giá cước tốt nhất (Rank 1) cho từng tuyến đường
SELECT 
    Rate_ID,
    Carrier,
    POL_Origin,
    POD_Destination,
    Container_Type,
    Ocean_Freight_USD,
    THC_USD,
    Seal_Fee_USD,
    Doc_Fee_USD,
    Total_Cost_USD,
    Quoted_Price_USD,
    Expected_Profit_USD,
    Valid_From,
    Valid_To,
    Transit_Time_Days,
    Rate_Status
FROM 
    RankedRates
WHERE 
    rate_rank = 1;