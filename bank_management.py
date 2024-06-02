
class Bank:
    def __init__(self, name) -> None:
        self.name= name
        self.__balance= 0
        self.__total_loaned= 0
        self.__users= {} #{ac_no: user_obj}
        self.__loan_feature= True

    def receiver_transaction(self, receiver, history):
        receiver.transation_history_added(history)

    def add_user(self, user):
        id= f"{user.name.lower()}${len(self.__users)+1}"
        user.set_ac_no(id)
        self.__users[id]= user
        print(f"{user.name} is added as user with ac_no: {id}")

    def set_bank_balance(self, amount):
        self.__balance+=amount

    def set_bank_balance_2(self, amount):
        self.__balance-=amount

    def receiver(self, receiver_ac_no):
        if receiver_ac_no in self.__users.keys():
            return self.__users[receiver_ac_no]
        else:
            return None
        
    def set_total_loaned(self, amount):
        self.__total_loaned+=amount

    def get_user(self, user_ac_no):
        if user_ac_no in self.__users.keys():
            return self.__users[user_ac_no]
        else:
            print('Invalid user account number')

    # admin section

    def delete_user(self, user_ac_no):
        if user_ac_no in self.__users.keys():
            print(f'Account No: {user_ac_no} Name: {self.__users[user_ac_no].name} is deleted.')
            del self.__users[user_ac_no]
        else:
            print('User not found!')

    def get_users(self):
        print()
        print('Total users: ',len(self.__users))
        print('Users details: ')
        i=1
        for id, user in self.__users.items():
            print(f'{i}. Account_no: {id}, User Name: {user.name}, Email: {user.email}, Address: {user.address}, AC type: {user.account_type};')
            i+=1

    def getter_balance(self):
        return self.__balance
    
    def getter_total_loaned(self):
        return self.__total_loaned
    
    def set_loan_feature(self, flag):
        self.__loan_feature= flag
        if flag== True:
            print('Loan feature is updated to ON')
        else:
            print('Loan feature is updated to OFF')

    def get_loan_feature(self):
        return self.__loan_feature

class User:
    def __init__(self, name, email, address, account_type) -> None:
        self.name= name
        self.email= email
        self.address= address
        self.account_type= account_type
        self.__ac_no= None
        self.__ac_balance= 0
        self.__ac_loan= 0
        self.loan_times= 2
        self.__transation_his= []

    def transaction_history(self):
        return self.__transation_his
    
    def transation_history_added(self, history):
        self.__transation_his.append(history)

    def get_ac_no(self):
        return self.__ac_no

    def set_ac_no(self, newId):
        self.__ac_no= newId

    def get_ac_balance(self):
        return self.__ac_balance
    
    def get_ac_loan(self):
        return self.__ac_loan
    
    def deposite_amount(self, amount):
        if amount>0:
            self.__ac_balance+=amount
            AB.set_bank_balance(amount)
            self.__transation_his.append(f'{amount} BDT is deposited in AC No: {self.__ac_no}')
            print(f'{amount} BDT is deposited in AC No: {self.__ac_no}')
        else:
            print('Invalid amount')

    def withdraw(self, amount):
        if amount<=self.get_ac_balance():
            if amount>AB.getter_balance():
                print(f'Sorry! {AB.name} bank is bankrupt')
            else:
                self.__ac_balance-=amount
                AB.set_bank_balance_2(amount)
                self.__transation_his.append(f'{amount} BDT withdraw from AC No: {self.__ac_no}')
                print(f'{amount} BDT withdraw from AC No: {self.__ac_no}')
        else:
            print('Withdrawal amount exceeded')

    def send_money(self, receiver_ac_no, amount):
        receiver= AB.receiver(receiver_ac_no)
        if receiver:
            if self.__ac_balance>=amount:
                self.__ac_balance-= amount
                receiver.__ac_balance+= amount
                self.__transation_his.append(f'Send {amount} BDT successfully from {self.__ac_no} to {receiver.__ac_no}')
                AB.receiver_transaction(receiver,(f'Received {amount} BDT successfully from {self.__ac_no} to {receiver.__ac_no}'))
                print(f'Send {amount} BDT successfully from {self.__ac_no} to {receiver.__ac_no}')
            else:
                print('You have not enough money!')
        else:
            print('Invalid Receiver Account Number.')

    def take_loan(self, amount):
        if AB.get_loan_feature():
            if amount<=AB.getter_balance():
                if self.loan_times>0:
                    self.__ac_loan+=amount
                    self.__ac_balance+=amount
                    AB.set_total_loaned(amount)
                    AB.set_bank_balance_2(amount)
                    self.loan_times-=1
                    self.__transation_his.append(f'Account Number: {self.get_ac_no()} loaned {amount} BDT successfully')
                    print(f'Account Number: {self.get_ac_no()} loaned {amount} BDT successfully')
                else:
                    print('You are not eligible for loan')
            else:
                print('Bank has not enough money to loan you!')
        else:
            print('Loan feature is not Available!')

class Admin:
    def __init__(self, name, email, address) -> None:
        self.name= name
        self.email= email
        self.address= address
        
    def delete_user(self, user_ac_no):
        AB.delete_user(user_ac_no)

    def get_all_users_list(self):
        AB.get_users()

    def available_bank_balance(self):
        print('Available Bank Balance: ')
        print(AB.getter_balance())

    def total_loan_amount(self):
        print('Total loan amount: ')
        print(AB.getter_total_loaned())

    def loan_feature(self, flag):
        AB.set_loan_feature(flag)

AB= Bank('AB')

def User_interface():
    run= False
    c= int(input('1. Login Or 2. Signup: '))
    user= None
    if c==1:
        ac_no= input('Enter your account number: ')
        user= AB.get_user(ac_no)
        if user:
            run= True
            print('Welcome back to our Bank')
    elif c==2:
        print('Enter User\'s info: ')
        name= input('Name: ')
        email= input('Email: ')
        address= input('Address: ')
        ac_type=''
        while True:
            print('Enter your account type: ')
            print('1. Saving Account')
            print('2. Current Account')
            opt_type= int(input())
            if opt_type== 1:
                ac_type+='Saving Account'
                break
            elif opt_type== 2:
                ac_type+='Current Account'
                break
            else:
                print('Choose the correct type.')
        user= User(name, email, address, ac_type)
        AB.add_user(user)
        run= True
        print('Welcome to AB Bank!')
    else:
        print('Try Again')

    while run:
        print()
        print('1. Check Available Balance')
        print('2. Deposite')
        print('3. Withdraw')
        print('4. To Loan')
        print('5. Send Money')
        print('6. Check Transaction History')
        print('7. Exit')
        opt= int(input('Enter an Option: '))
        if opt== 1:
            print(f'Your current Balance is: {user.get_ac_balance()} BDT')
        elif opt==2:
            amount= int(input('Enter the amount: '))
            user.deposite_amount(amount)
        elif opt==3:
            amount= int(input('Enter the amount: '))
            user.withdraw(amount)
        elif opt==4:
            amount= int(input('Enter the amount: '))
            user.take_loan(amount)
        elif opt==5:
            receiver_ac_no= input('Enter the receiver account number: ')
            amount= int(input('Enter the amount: '))
            user.send_money(receiver_ac_no, amount)
        elif opt==6:
            print(f'Transaction history of Account Number {user.get_ac_no()}: ')
            print(user.transaction_history())
        elif opt==7:
            print('Exited')
            break
        else:
            print('Invalid option!')

def admin_interface():
    print('Enter Admin\'s info: ')
    name= input('Name: ')
    email= input('Email: ')
    address= input('Address: ')
    admin= Admin(name, email, address)
    print('Welcome to AB Bank admin panel!')
    print()
    while True:
        print()
        print('1. Delete User')
        print('2. See All Users')
        print('3. Total Bank Balance')
        print('4. Total Loan Amount')
        print('5. Loan Feature Change')
        print('6. Exit')
        opt= int(input('Enter an option: '))
        if opt==1:
            user_ac_no= input('Enter the user account number: ')
            admin.delete_user(user_ac_no)
        elif opt==2:
            admin.get_all_users_list()
        elif opt==3:
            admin.available_bank_balance()
        elif opt==4:
            admin.total_loan_amount()
        elif opt==5:
            print('1. Turn ON')
            print('2. Turn OFF')
            ch= int(input('Enter your choise: '))
            if ch==1:
                admin.loan_feature(True)
            elif ch==2:
                admin.loan_feature(False)
            else:
                print('Invalid choise. Try again.')
        elif opt==6:
            print('Exited.')
            break

while True:
    print('1. Use as User')
    print('2. Use as Admin')
    print('3. Exit')
    opt= int(input('Enter an option: '))

    if opt==1:
        User_interface()
    elif opt==2:
        admin_interface()
    elif opt==3:
        print('Exited')
        break
    else:
        print('Invalid option!')

