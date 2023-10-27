def info(**args):
    return """

    ***** Service command *****
    "close", "exit", "." --> Exit from AddressBook
    
    ***** Add/edit command *****
    "add" name phone                  --> Add contact to AddressBook
    "change" name old_phone new_phone --> Change the contacts phone number
    "addbd" name birthday             --> Add/edit contact birthday
    "fake" bool                       --> Makes the specified number of contacts
    
    ***** Delete command *****
    "del" name phone to remove --> Delete old phone number
    "delete" name              --> Delete contact
    "boom"                     --> Delete all contacts
    
    ***** Info command *****
    
    "all"             --> Show all contacts info
    "phone" name      --> Show contacts phone
    "showbd" name     --> Show when day to contact birthday
    "bd"              --> Show a list of contacts to congratulate by day of the week.
    "help" / "info"   --> Commands list
    
"""
