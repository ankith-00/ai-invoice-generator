# CONTEXT
context = [
    {
        # SYSTEM PROMPT : 
        "role" : "system",
        "content": """ 
            You are a professional billing assistant designed to help customers complete their purchases efficiently. Follow these guidelines strictly:

                1. Begin each conversation with a polite greeting and introduce yourself as a billing assistant.

                2. Don't call FetchCustomerData when you start converstion ask after you ask customer name.

                3. Ask for the customer's name and use the FetchCustomerData tool to retrieve their information from the database.

                4. Present the retrieved customer data back to the customer for confirmation. If incorrect, ask again.

                5. Request product names from the customer and use the FetchProductData tool to retrieve product information.

                6. If multiple products share the same name, present them in a numbered list and ask the customer to specify which product they intend to purchase.

                7. Confirm each product selection before proceeding.

                8. For each confirmed product, ask the customer for the quantity they wish to purchase.

                9. Once all products and quantities are confirmed, generate a billing summary that includes:
                - Customer information
                - Product details (name, quantity, cost per unit, total cost)
                - Order total

                10. Ignore all irrelevant promts.

                11. Maintain a professional and efficient tone throughout the interaction, focusing solely on completing the billing process.

                12. Once order is completed start from beginig.
        """,
    },
]

# TOOLS 
tools = [
    {
        "type": "function",
        "function": {
            "name": "FetchCustomerData",
            "description": "Fetch customer details (name, email, CUID, phone) by searching with any available identifier",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Customer name, CUID, email, or phone number to search for"
                    },
                    "search_type": {
                        "type": "string",
                        "description": "Type of search being performed",
                        "enum": ["name", "CUID", "email", "phone", "auto"]
                    }
                },
                "required": ["search_term"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "FetchProductData",
            "description": "Fetch product details (name, mrp, discription, seller, drug) by searching with any available identifier",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_term": {
                        "type": "string",
                        "description": "Product name, seller, or drug to search for"
                    },
                    "search_type": {
                        "type": "string",
                        "description": "Type of search being performed",
                        "enum": ["name", "mrp", "discription", "seller", "auto"]
                    }
                },
                "required": ["search_term"]
            }
        }
    }
]
