import functools

def determineAuthorization(doc_clearance_level):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            clearance_levels = {"top_secret":["top_secret"],
                                "secret":["top_secret", "secret"],
                                "confidential":["top_secret", "secret", "confidential"]}
    
            user_data = kwargs.get('user_data', None)
            full_name = user_data.get('full_name').lower()
            user_clearance_level = user_data.get('user_clearance_level').lower()
            allowed_level = clearance_levels.get(doc_clearance_level, [])
            print(user_clearance_level)
            print(allowed_level)        
            if user_clearance_level in allowed_level:
                print(f"✅ [GRANTED] {full_name} ({user_clearance_level}) is authorized for {doc_clearance_level} content.")
                return func(*args, **kwargs)
            else:
                print(f"❌ [DENIED] {full_name} ({user_clearance_level}) does not have {doc_clearance_level} clearance.")

        return wrapper
    return decorator

@determineAuthorization('top_secret')
def viewTopSecretDocument(user_data=None):
    print("The nuclear missles secret code is [1 2 3 4 5]")

@determineAuthorization('secret')
def viewSecretDocument(user_data=None):
    print("The white house has secret tunnels")

@determineAuthorization('confidential')
def viewConfidentialDocument(user_data=None):
    print("Aliens have never been found")

user1_data={"full_name":"Steve Correa","user_clearance_level":"top_secret"}
viewTopSecretDocument(user_data=user1_data)
print("*"*40)
viewSecretDocument(user_data=user1_data)
print("*"*40)
viewConfidentialDocument(user_data=user1_data)
