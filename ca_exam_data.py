data = {
    "Group I": {
        "Advance Accounting": {
            "AS-1: Accounting Policies": 1,
            "AS-2: Valuation of Inventories": 4,
            "AS-3: Cash Flow Statements": 8,
            "AS-4: Contingencies & Events after Balance Sheet Date": 2,
            "AS-5: Net Profits": 2,
            "AS-7: Construction Contracts": 4,
            "AS-9: Revenue Recognition": 1,
            "AS-10: Property, Plant and Equipment": 3,
            "AS-11: Effects of Changes in Foreign Exchange Rates": 4,
            "AS-12: Government Grants": 3,
            "AS-13: Investments": 6,
            "AS-14: Amalgamation of Companies": 14,
            "AS-15: Retirement Benefits": 2,
            "AS-16: Borrowing Costs": 6,
            "AS-17: Segment Reporting": 2,
            "AS-18: Related Party Disclosures": 2,
            "AS-19: Leases": 6,
            "AS-20: Earnings Per Share": 4,
            "AS-21: Consolidated Financial Statements": 12,
            "AS-22: Accounting for Taxes on Income": 3,
            "AS-23: Accounting for Investments in Associates": 2,
            "AS-24: Discontinuing Operations": 2,
            "AS-25: Interim Financial Reporting": 2,
            "AS-26: Intangible Assets": 3,
            "AS-27: Joint Ventures": 2,
            "AS-28: Impairment of Assets": 2,
            "AS-29: Provisions, Contingent Liabilities & Contingent Assets": 2,
            "Schedule III": 2,
            "Company Final Accounts": 12,
            "Buy Back of Shares": 4,
            "Internal Reconstruction": 8,
            "Branch Accounting": 16
        },
        # Priority lists for Advance Accounting based on image_cc95f9.png
        "Advance Accounting_High_Importance": [
            "Branch Accounting",
            "Internal Reconstruction",
            "AS-14: Amalgamation of Companies",
            "AS-3: Cash Flow Statements",
            "AS-13: Investments",
            "Buy Back of Shares",
            "Company Final Accounts",
            "AS-4: Contingencies & Events after Balance Sheet Date", # Added from image
            "AS-5: Net Profits", # Added from image
            "AS-10: Property, Plant and Equipment", # Added from image
            "AS-11: Effects of Changes in Foreign Exchange Rates", # Added from image
            "AS-16: Borrowing Costs", # Added from image
            "AS-18: Related Party Disclosures", # Added from image
            "AS-25: Interim Financial Reporting" # Added from image
        ],
        "Advance Accounting_Medium_Importance": [
            "AS-21: Consolidated Financial Statements",
            "AS-22: Accounting for Taxes on Income",
            "AS-15: Retirement Benefits",
            "AS-19: Leases",
            "AS-20: Earnings Per Share",
            "AS-26: Intangible Assets",
            "AS-28: Impairment of Assets",
            "Schedule III"
        ],
        "Advance Accounting_Least_Importance": [
            "AS-23: Accounting for Investments in Associates",
            "AS-27: Joint Ventures",
            "AS-1: Accounting Policies",
            "AS-2: Valuation of Inventories",
            "AS-7: Construction Contracts",
            "AS-9: Revenue Recognition",
            "AS-12: Government Grants",
            "AS-17: Segment Reporting",
            "AS-24: Discontinuing Operations",
            "AS-29: Provisions, Contingent Liabilities & Contingent Assets"
        ],
        "Corporate and Other Laws": {
            "Preliminary": 2.5,
            "Inc of Co. & Matters Incidental thereto": 5,
            "Prospectus and allotment of securities": 4,
            "Share Capital & Debentures": 5,
            "Acceptance of Deposits by Cos": 3,
            "Regitration of Charges": 2.5,
            "Mgmt & Adminstration": 7,
            "Declaration and Payment of Dividend": 3,
            "Accounts of Companies": 6,
            "Audit & Auditors": 5,
            "Cos Incorporated outside India": 2,
            "The LLP Act, 2008": 4,
            "The FEMA, 1999": 3.5,
            "The GCA, 1897": 3.5,
            "Interpretation of Statutes": 3.5
        },
        # Placeholder importance lists for Corporate and Other Laws
        "Corporate and Other Laws_High_Importance": [
            "Share Capital & Debentures",
            "Mgmt & Adminstration",
            "Accounts of Companies",
            "Audit & Auditors"
        ],
        "Corporate and Other Laws_Medium_Importance": [],
        "Corporate and Other Laws_Least_Importance": [],
        "Taxation": { # This is a meta-subject containing sub-subjects
            "Income Tax": {
                "Basic Concepts": 2,
                "Residence & Scope of Total Income": 2,
                "Income from Salary": 4,
                "Income from House Property": 2,
                "PGBP": 8,
                "Capital Gain": 8,
                "IFOS": 4,
                "Income of other persons included in Assessee's Total Income": 2,
                "Set off and Carry forward losses": 2,
                "Deduction from GTI": 6,
                "Adv Tax, TDS and TCS": 5,
                "Prov for filing return of Income and Self Assessment": 2,
                "Income Tax Liability Computation and Optimisation": 10
            },
            # Placeholder importance lists for Income Tax
            "Income Tax_High_Importance": [
                "PGBP",
                "Capital Gain",
                "Deduction from GTI",
                "Income Tax Liability Computation and Optimisation"
            ],
            "Income Tax_Medium_Importance": [],
            "Income Tax_Least_Importance": [],
            "GST": {
                "Introduction and Constitution": 0.5,
                "Definitions": 0.5,
                "Chargeability and Goods & Services": 0.75,
                "Supply": 1,
                "Place of supply": 1,
                "Taxable Person": 0.75,
                "Exemption": 3,
                "Valuation": 0.75,
                "Reverse Charge Mechanism": 2,
                "Invoice": 0.75,
                "Time of Supply": 0.5,
                "Registration": 1,
                "Input Tax Credit": 2,
                "Manner of Payment": 0.5,
                "TDS, TCS": 0.75,
                "Filing of Return": 0.5,
                "Accounts and Records": 0.5,
                "E-Way Bill": 0.5
            },
            # Placeholder importance lists for GST
            "GST_High_Importance": [
                "Taxable Person",
                "Registration",
                "Supply",
                "Input Tax Credit",
                "Reverse Charge Mechanism",
                "Exemption",
                "Place of supply",
                "Time of Supply",
                "Valuation"
            ],
            "GST_Medium_Importance": [
                "E-Way Bill",
                "TDS, TCS",
                "Invoice",
                "Manner of Payment"
            ],
            "GST_Least_Importance": [
                "Introduction and Constitution",
                "Definitions",
                "Chargeability and Goods & Services",
                "Filing of Return",
                "Accounts and Records"
            ]
        }
    },
    "Group II": {
        "Auditing and Ethics": {
            "Nature, Objectives & Scope of Audit": 4.5,
            "Audit Strategy, Planning & Programme": 2,
            "Audit Documentation": 1,
            "Risk Assessment & Internal Control": 3,
            "Audit Procedures": 1,
            "SA 320 / 450 / 530": 3.5,
            "Automated Environment": 1.5,
            "SA 500 / 501 / 505 / 510": 3.5,
            "SA 550 / 560 / 570 / 580": 3,
            "Communication with Mgmt & TCWG (SA 260 / 265)": 1,
            "Analytical Procedures": 1,
            "Audit Report (SA 700 / 701 / 705 / 706 / 710), Branch Audit & SA 600, SA 299": 5,
            "CARO & Company Audit": 1.5,
            "Bank Audit": 3,
            "Government Audit": 1,
            "Cooperative Society Audit": 1,
            "Other Entities Audit": 3,
            "Audit of Items of Financial Statements": 6,
            "Internal Audit & SA 610": 1
        },
        # Placeholder importance lists for Auditing and Ethics
        "Auditing and Ethics_High_Importance": [
            "Audit Report (SA 700 / 701 / 705 / 706 / 710), Branch Audit & SA 600, SA 299",
            "Bank Audit",
            "Audit of Items of Financial Statements"
        ],
        "Auditing and Ethics_Medium_Importance": [],
        "Auditing and Ethics_Least_Importance": [],
        "Cost and Management Accounting": {
            "Intro to CMA": 3,
            "Material Cost": 7,
            "Employee Cost": 6,
            "Overheads-Absorption Costing Method": 7.5,
            "Activity Based Costing": 6,
            "Cost Sheet": 5,
            "Cost Accounting System": 6,
            "Unit and Batch Costing": 3.5,
            "Job Costing": 2.5,
            "Process and Operation Costing": 6.5,
            "Joint & By Products": 5,
            "Service Costing": 7.5,
            "Standard Costing": 8.5,
            "Marginal Costing": 9,
            "Budget and Budgetary Controls": 8
        },
        # Placeholder importance lists for Cost and Management Accounting
        "Cost and Management Accounting_High_Importance": [
            "Material Cost",
            "Activity Based Costing",
            "Process and Operation Costing",
            "Standard Costing",
            "Marginal Costing",
            "Budget and Budgetary Controls"
        ],
        "Cost and Management Accounting_Medium_Importance": [],
        "Cost and Management Accounting_Least_Importance": [],
        "FMSM": {
            "FM": {
                "Scope and Objectives of FM": 1.5,
                "Types of Financing": 2,
                "Ratio Analysis": 3.5,
                "Cost of Capital": 4,
                "Capital Structure": 4,
                "Leverage": 4,
                "Investment Decisions- Capital Budgeting": 4,
                "Dividend Decisions": 4,
                "Management of Working Capital": 4
            },
            # Placeholder importance lists for FM
            "FM_High_Importance": [
                "Ratio Analysis",
                "Cost of Capital",
                "Capital Structure",
                "Leverage",
                "Investment Decisions- Capital Budgeting",
                "Management of Working Capital"
            ],
            "FM_Medium_Importance": [],
            "FM_Least_Importance": [],
            "SM": {
                "Introduction to Strategic Management": 6,
                "Strategic Analysis: External Environment": 6,
                "Strategic Analysis: Internal Environment": 6,
                "Strategic Choices": 7,
                "Strategy Implementation & Evaluation": 10
            },
            # Placeholder importance lists for SM
            "SM_High_Importance": [
                "Strategic Choices",
                "Strategy Implementation & Evaluation"
            ],
            "SM_Medium_Importance": [],
            "SM_Least_Importance": []
        }
    }
}
