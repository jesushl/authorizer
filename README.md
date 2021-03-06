# Authorizer
> Authorizer is a tool to handle two different transaction operations.
> 1. Account Creation
> 2. Transaction authorization for the account

## How it works
> This origram can read transactions in **json** format from **stdin** and **return a json** response at **stdout**. For practical focus testing read a file with pre loaded examples.

Every operation is read it with this format, amount are only positive integers.
```
# for account actions
{"account": {"active_card":<boolean>, "available-limit": <int_amount>}}
# for transactions
{"transaction": {"merchant": <str_merchant_name>, "amount": <int_amount>, "time": <timestamp>}}
```
This return a line by every action as log message with this format
```
{"account": {"active-card": <boolean>, "available-limit": <int_amount>}, "violations": [<str_viloation>, ...]}
```
### How to run it

In order to have the expected input you can add an alias to the python code like
```
alias operations="./operations.sh"
``` 
Also you can run the docker image in Authorizer/Dockerfile
using 
```
docker build -t operations_jjhl Autorizer/.
docker run  -it -did --name operations_jjhl operations_jjhl 
```
Can connect into the container using 
```
docker exec -it operations_jjhl bash
```
And run an example if you like 
```
operations < tests/text_examples/test_input_file.txt 
```

### Rules
* No transaction should be accepted without a properly initialized account: **account-not-initialized**
* No transaction should be accepted when the card is not active: **card-not-active**
* The transaction amount should not exceed the available limit: **insufficient-limit**
* There should be no more than 3 transactions within a 2 minutes interval: **high-frequency-small-interval**
* There should be no more than 1 similar transaction (same amount and merchant) within a 2 minutes interval:
**doubled-transaction**

### State
This program not uses an external database, for this reason all states and transactins are build it in an internal group of collections, specially use dictionaries that share objects in order to increase the speed


## Design

### Data structures
As database is not abailable, a concept as documents in noSQL is very used with json formats, but our current input structure has not a good search performance.

#### Account
 Account is a register that is created before transactions, this register cant be re-created or edited. This is the initial status for available limit on account.

 #### Transactions 
 All valid transactions should be created after an account creation. By now all transctions are disbursments and arrives consecutively

 #### Input 
 As this program requires read a file from command line, for this reason use argparser sounds good

 #### Sequence 
 <sub>Validator represents a set of validators by account or transaction</sub>
 ```mermaid
    sequenceDiagram
    Stdin ->> Authorizator:"{<account>}"
    Authorizator ->> Validator: Is created before?
    Validator -->> Authorizator: Violations
    Validator -->> Validator: Preserve account state 
    Authorizator ->> Stdout: Account operation output
    Stdin ->> Authorizator: "{transaction}"
    Authorizator ->> Validator: This transaction has an account related?
    Authorizator ->> Validator: Related account is active?
    Authorizator ->> Validator: Amount not exceed account limit?
    Authorizator ->> Validator: Previous 2 transactions was made in less of 2 minutes?
    Authorizator ->> Validator: Similar transaction with amounth and merchand happend with 2 minutes interval?
    Validator -->> Authorizator: Violations
    Validator -->> Validator: Preserve transaction state    
    Authorizator ->> Stdout: Transaction operation output
 ```

### Clases

```mermaid
    classDiagram
class Authorizator {
  str input_arg
  TransactionValidator transaction_validator
  AccountValidator account_validator
  read_args()
  validate_account()
  validate_transaction()
  return_account_status()
  return_transaction_status()
}
class Validator{
    violations: list <str>
    get_status()
    verify()
}
class AccountValidator{
    exists_a_valid_account()
    verify()
    Account account
}
class TransactionValidator{
    account: Account
    Transaction transaction
    List <Transaction> historic_transactions
    set_account()
    verify_initialized_account()
    verify_card_active()
    verify_limit()
    verify_hight_frecuency_interval()
    verify_dobled_transaction()
    verify()

}
class Account{
    is_active: bool
    available_limit: int
    __init__(<json_account>)
    disbursment(amount)
}
class Transaction{
    int amount
    str merchant
    datetime timestamp
    Account account 
}
TransactionValidator o--Transaction
TransactionValidator o-- Account
AccountValidator o-- Account
Transaction o-- Account
Validator <|-- AccountValidator
Validator <|-- TransactionValidator
Authorizator --* TransactionValidator
Authorizator --* AccountValidator
```
x
