from flask import Flask, render_template, request, redirect, g, url_for
from flask_bootstrap import Bootstrap
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import pprint
import json

url = "https://ropsten.infura.io/v3/8db3e633846f4c7e8d02c53a00253acc"
w3 =  Web3(HTTPProvider(url))

print(f"connection : {w3.isConnected()}")

app = Flask(__name__)
bootstrap = Bootstrap(app)

contract_address = w3.toChecksumAddress("0xc2cc247ff4707afAc61521adC31C5CEDF77c548E")

contract_abi = [
                {
                    "inputs": [],
                    "stateMutability": "nonpayable",
                    "type": "constructor"
                },
                {
                    "inputs": [
                        {
                            "internalType": "string",
                            "name": "userJsonData",
                            "type": "string"
                        }
                    ],
                    "name": "addUserData",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "changeStatus",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "numOfUsers",
                    "outputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "owner",
                    "outputs": [
                        {
                            "internalType": "address",
                            "name": "",
                            "type": "address"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "status",
                    "outputs": [
                        {
                            "internalType": "bool",
                            "name": "",
                            "type": "bool"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                    ],
                    "name": "userList",
                    "outputs": [
                        {
                            "internalType": "string",
                            "name": "",
                            "type": "string"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
'''contract_abi = [
                {
                    "inputs": [],
                    "stateMutability": "nonpayable",
                    "type": "constructor"
                },
                {
                    "inputs": [
                        {
                            "internalType": "string",
                            "name": "userJsonData",
                            "type": "string"
                        }
                    ],
                    "name": "addUserData",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "changeStatus",
                    "outputs": [],
                    "stateMutability": "nonpayable",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "numOfUsers",
                    "outputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "owner",
                    "outputs": [
                        {
                            "internalType": "address",
                            "name": "",
                            "type": "address"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [],
                    "name": "status",
                    "outputs": [
                        {
                            "internalType": "bool",
                            "name": "",
                            "type": "bool"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                },
                {
                    "inputs": [
                        {
                            "internalType": "uint256",
                            "name": "",
                            "type": "uint256"
                        }
                    ],
                    "name": "userList",
                    "outputs": [
                        {
                            "internalType": "string",
                            "name": "",
                            "type": "string"
                        }
                    ],
                    "stateMutability": "view",
                    "type": "function"
                }
            ]
'''
contract = w3.eth.contract(address = contract_address, abi = contract_abi)

print(contract.all_functions())
print("Owner Account : "+contract.functions.owner().call())

owner_pub_key = "0xd6bf36879D1943C6Ade5a34a48bada68A0fbC9Dd"
owner_pri_key = "BA988B7C6623100CC7A06B1C798382B724189406C5623ED466B0B4855D08655F"

@app.route("/")
def homePage():

    return redirect(url_for("home_page"))


@app.route("/homePage")
def home_page():
#options to log in
#button to see userData page 

    return render_template("homePage.html")

@app.route("/addDataForm",  methods=["GET", "POST"])
def add_data_form():#get and post methods to get the login details

    return render_template("addDataForm.html")

@app.route("/transact", methods=["GET", "POST"])
def transact():

    name = request.form["name"]
    DOB = request.form["DOB"]
    mailID = request.form["mailID"]
    contactNumber = request.form["contactNumber"]
    gender = request.form["gender"]
    idType = request.form["idType"]
    idNo = request.form["idNo"]
    houseNo = request.form["houseNo"]
    district = request.form["district"]
    city_state = request.form["city-state"]
    about = request.form["about"]
    qualification = request.form["qualification"]
    
    jsonData = {

        'name': name,
        'DOB': DOB,
        'mailID': mailID,
        'contactNumber': contactNumber,
        'gender': gender,
        'idType': idType,
        'idNo': idNo,
        'houseNo': houseNo,
        'district': district,
        "city_state": city_state,
        'about': about,
        'qualification': qualification
    }
    
    jsonDataString = json.dumps(jsonData)
    print("JSON data string : "+jsonDataString)

    transaction = contract.functions.addUserData(jsonDataString).buildTransaction({
        'gas': 1000000,
        'gasPrice': Web3.toWei('1', 'gwei'),
        'from': owner_pub_key,
        'nonce': w3.eth.getTransactionCount(owner_pub_key)
    })

    ###############################EXECUTED################################
    signed_txn = w3.eth.account.signTransaction(transaction, private_key=owner_pri_key)
    tx = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    #############################################################
    tx_hash = w3.toHex(tx)
    print("tx_hash = "+tx_hash)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("\n\nTransaction receipt mined:")
    pprint.pprint(dict(receipt))
    print("\n\nWas transaction successful?")
    status = receipt['status']
    pprint.pprint(status)


    #return redirect(url_for("home_page"))
    if status == 1:
        return render_template("dataSaved.html", tx_hash = tx_hash )

    else:
        return render_template("addDataForm.html",status = status)


@app.route("/userData")
def userData():
    numOfUsers = contract.functions.numOfUsers().call()
    print(f"\nNo. of registered users : {numOfUsers}")


    userDataList = []
    for i in range(numOfUsers):
        userDataList.append(json.loads(contract.functions.userList(i).call()))


    print("\nUser Data List.... :")
    print(userDataList)
    #require number of users
    #then we'll fetch the details of each user

    return render_template("userData.html", numOfUsers = numOfUsers, userDataList  = userDataList)#we'll pass the user list along with it...