import sys
import json
with open ("users.json") as users_file:
    users = json.load(users_file)

with open ("tickets.json") as tickets_file:
    tickets = json.load(tickets_file)

with open ("organizations.json") as organizations_file:
    organizations = json.load(organizations_file)


print("-" * 40)
print("Type 'quit' to exit at any time, Press 'Enter' to continue")
options_string = "\n Select search options: \n * Press 1 to search Zendesk \n * Press 2 to view a list of searchable fields \n * Type 'quit' to exit"
options = options_string.center(10)
print(options)

##########################################################################################
selected_option = input()
if str(selected_option) not in ["1", "2", "quit"]:
    print("invalid option selected")
else:
    if str(selected_option) == "1":
        print ("Select 1) Users or 2) Tickets or 3) Organizations")
        category = input()
        if str(category) not in ["1", "2", "3", "quit"]:
            print("Invalid category selected")
        else:
            if category == "quit":
                sys.exit()
            else:    
                print ("Enter search term")
                search_term = input()
                if search_term == "":
                    print("Search term cannot be empty")
                elif search_term == "quit":
                    sys.exit()
                else:
                    print ("Enter search value")
                    search_value = input()
                    if search_value == "quit":
                        sys.exit()
##########################################################################################
                if str(category) == "1":
                    category_object = users
                    category_type = "users"
                elif str(category) == "2":
                    category_object = tickets
                    category_type = "tickets"
                elif str(category) == "3":
                    category_object = organizations
                    category_type = "organizations"

                   
                print("Searching " + category_type + " for " + str(search_term) + " with a value of " + str(search_value))
                records_count = 0
                invalid_search_term = False
                for object in category_object:
                    if search_term in object:
                        if str(object[search_term]).lower() == str(search_value).lower():
                            records_count += 1
                            for key, value in object.items():
                                print(key.ljust(20) , value)                              
                                assigned_tickets = []   
                                for ticket in tickets:
                                    if "organization_id" in ticket:
                                        if category_type == "users" :
                                            if ticket["submitter_id"] == object["_id"]:
                                                assigned_tickets.append(ticket["subject"])
                                        elif category_type == "organizations" :
                                            if ticket["organization_id"] == object["_id"]:
                                                assigned_tickets.append(ticket["subject"])

                                organization_name = ""
                                for organization in organizations:
                                    if category_type == "users" or category_type == "tickets":
                                            if organization["_id"] == object["organization_id"]:
                                                organization_name = organization["name"]
                                            
                                organization_users = []
                                assignee_name = ""
                                submitter_name = ""
                                for user in users:
                                    if category_type == "organizations":
                                        if "organization_id" in user:
                                            if user["organization_id"] == object["_id"]:
                                                organization_users.append(user["name"])
                                    elif category_type == "tickets":
                                        if user["_id"] == object["assignee_id"]:
                                            assignee_name = user["name"]
                                        if user["_id"] == object["submitter_id"]:
                                            submitter_name = user["name"]

                            if assigned_tickets:
                                i = 0
                                for assigned_ticket in assigned_tickets:
                                    i += 1
                                    ticket_index = "ticket_" + str(i)
                                    print(ticket_index.ljust(20) , assigned_ticket)
                            if organization_users:
                                j = 0
                                for organization_user in organization_users:
                                    j += 1
                                    user_index = "user_" + str(j)
                                    print(user_index.ljust(20) , organization_user)
                            if assignee_name and submitter_name:
                                print("assignee_name".ljust(20) , user["name"])
                                print("submitter_name".ljust(20) , user["name"])
                            
                            if organization_name:
                                print("organization_name".ljust(20) , organization_name)
                            print('-' * 40)
                    else:
                        invalid_search_term = True
                        
                if invalid_search_term == True:
                    print("Invalid search term")
                if records_count <= 0:
                    print("No results found")

##########################################################################################                    
    elif selected_option == "2":
        print("-" * 40)
        print("Search Users with")
        for key in users[0].keys():
            print (key)
            
        print("-" * 40)
        print("Search Tickets with")
        for key in tickets[0].keys():
            print (key)

        print("-" * 40)
        print("Search Organizations with")
        for key in organizations[0].keys():
            print (key)



