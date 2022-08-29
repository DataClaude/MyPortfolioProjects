welcome = "Welcome to the tip calculator!"
print(welcome)
bill = input("What was the total bill? $")
tip = input("How much will you like to tip/? 10, 12 or 15%? ")
split_bill = input("How many people to split the bill? ")

bill_paid = float(bill)
tip_percent = float(tip) / 100
number_split = int(split_bill)
total_tip = tip_percent * bill_paid
total_bill = (bill_paid + total_tip) / number_split
final_amount = "{:.2f}".format(total_bill)

message = f"Each person is to pay ${final_amount}"
print(message)
