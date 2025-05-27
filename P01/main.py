# AUTHOR : ANKITH KUMAR 
# DETERMINENT STUDIOS ~ INTERNSHIP PROJECT
import json
from groq import Groq
from dotenv import load_dotenv
from utility import context , tools


# - - - - LODING ENV DATA - - - - #
load_dotenv()

# - - - - CREATING 'GROQ' CLIENT - - - - #
client = Groq()

Customer_Data_FilePath = 'CustomerData.json'
Product_Data_filePath = 'ProductList.json'



# - - - - - FUNCTION TO FETCH 'CUSTOMER_DATA' FROM 'DB' - - - - -  #
def FetchCustomerData(CustomerName):
        with open(Customer_Data_FilePath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        CustName = CustomerName.get('search_term', '').strip().lower()
        
        # SEARCHING CUSTOMER NAME
        results = [item for item in data if CustName in item.get("name", "").lower()]

        return results



# - - - - - FUNCTION TO FETCH 'PRODUCT_DATA' FROM 'DB' - - - - -  #
def FetchProductData(ProductName):
        with open(Product_Data_filePath, 'r', encoding='utf-8') as file:
            data = json.load(file)

        ProName = ProductName.get('search_term', '').strip().lower()
        
        # SEARCHING PRODUCT NAME
        results = [item for item in data if ProName in item.get("name", "").lower()]

        return results




# - - - - - FUNCTION TO FUNCTION BASED ON REQUEST - - - - -  #
def process_tool_call(tool_name, tool_input):
    if tool_name == "FetchCustomerData":
        return FetchCustomerData(tool_input)
    elif tool_name == "FetchProductData":
        return FetchProductData(tool_input)
    else:
         print('NO SUCH TOOL EXIST !')




# - - - - - FUNCTION TO CALL AI TO GENERATE RESPONSE - - - - -  #
def CallAI(UserInput):
    completion = client.chat.completions.create(
        messages= UserInput,
        model="llama3-70b-8192",
        tools=tools,
    )
    return completion




# - - - - - - MAIN - - - - - - - #
while True:
    UserInput = input('USER : ') 

    # - - - - IF USER INPUT 'EXIT' LOOP BREAK - - - - - - # 
    if UserInput.lower() == 'exit':
        break
    else:
        # - - - - CONTEXT UPDATING WITH 'UserInput' - - - - #
        InputToAI = {"role": "user", "content": UserInput}
        context.append(InputToAI)

        # - - - CALLING AI - - - #
        response = CallAI(context)


        # - - - - - - - IF TOOL CALL DETECTED ! - - - - - - - - #
        while response.choices[0].finish_reason == "tool_calls":  

            # print('TOOLS CALL DETECTED !')

            tool_calls = response.choices[0].message.tool_calls

            context.append({
                "role": "assistant", 
                "content": response.choices[0].message.content,
                "tool_calls": [tool_call.model_dump() for tool_call in tool_calls]
            })

            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # GET FUNCTION RESULT
                result = process_tool_call(function_name, function_args)
                
                context.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })
            
            # - - - - - GET NEW RESPONSE - - - - - #
            response = CallAI(context)

    # - - - - - - - - - - - - - PRINT AI RESPONSE - - - - - - - - - - - - - - - - #
    print('AI : ', response.choices[0].message.content)
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  \n')
