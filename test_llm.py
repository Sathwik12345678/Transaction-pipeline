from app.services.llm_service import generate_summary

response = generate_summary("""
Total INR Spend: 45000
Total USD Spend: 100
Top Merchants: Amazon, Swiggy
Anomalies Found: 5

Generate a spending summary and risk level.
""")

print(response)