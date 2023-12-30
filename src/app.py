from flask import Flask,render_template,request,redirect
import json
from web3 import Web3,HTTPProvider

def connect_with_farmer(wallet):
    blockchain="http://127.0.0.1:7545"
    web3=Web3(HTTPProvider(blockchain))
    print('Blockchain Server Connected')
    if wallet==0:
        web3.eth.defaultAccount=web3.eth.accounts[0]
    else:
        web3.eth.defaultAccount=wallet
    
    with open("../build/contracts/farmer.json") as f:
        artifact=json.load(f)
        abi=artifact['abi']
        address=artifact['networks']['5777']['address']
    
    contract=web3.eth.contract(abi=abi,address=address)
    print('contract selected')
    return contract,web3

app=Flask(__name__)

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/farmer')
def farmerPage():
    contract,web3=connect_with_farmer(0)
    _farmers,_farmernames=contract.functions.viewFarmer().call()
    print(_farmers,_farmernames)
    l=len(_farmers)
    data=[] # [['madhu','0x111..'],['numi','0x22..']]
    for i in range(l):
        dummy=[]
        dummy.append(_farmernames[i])
        dummy.append(_farmers[i])
        data.append(dummy)

    return render_template('farmer.html',num=l,data=data)

@app.route('/distributor')
def distributorPage():
    contract,web3=connect_with_farmer(0)
    _distributors,_distributornames=contract.functions.viewDistributor().call()
    print(_distributors,_distributornames)
    l=len(_distributors)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_distributornames[i])
        dummy.append(_distributors[i])
        data.append(dummy)

    return render_template('distributor.html',num=l,data=data)

@app.route('/shop')
def shopPage():
    contract,web3=connect_with_farmer(0)
    _shops,_shopnames=contract.functions.viewShop().call()
    print(_shops,_shopnames)
    l=len(_shops)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_shopnames[i])
        dummy.append(_shops[i])
        data.append(dummy)
    return render_template('shop.html',num=l,data=data)

@app.route('/asset')
def assetPage():
    contract,web3=connect_with_farmer(0)
    _assetid,_assetf,_assetd,_assets=contract.functions.viewAsset().call()
    print(_assetid,_assetf,_assetd,_assets)
    _farmers,_farmernames=contract.functions.viewFarmer().call()
    _distributors,_distributornames=contract.functions.viewDistributor().call()
    _shops,_shopnames=contract.functions.viewShop().call()
    print(_farmers,_farmernames)
    print(_distributors,_distributornames)
    print(_shops,_shopnames)
    l=len(_assetid)
    data=[]
    for i in range(l):
        dummy=[]
        dummy.append(_assetid[i])
        findex=_farmers.index(_assetf[i])
        dummy.append(_farmernames[findex])
        if _assetf[i]==_assetd[i]:
            dummy.append("not dispatched")
        else:
            dindex=_distributors.index(_assetd[i])
            dummy.append(_distributornames[dindex])
        if _assetf[i]!=_assetd[i] and _assetf[i]==_assets[i]:
            dummy.append("In Warehouse")
        elif _assetf[i]!=_assets[i]:
            sindex=_shops.index(_assets[i])
            dummy.append(_shopnames[sindex])
        else:
            dummy.append("not dispatched")
        data.append(dummy)
    return render_template('asset.html',num=l,data=data)

@app.route('/indexdata',methods=['post'])
def indexdata():
    assetid=int(request.form['assetid'])
    print(assetid)
    contract,web3=connect_with_farmer(0)
    _assetid,_assetf,_assetd,_assets=contract.functions.viewAsset().call()
    print(_assetid,_assetf,_assetd,_assets)
    if assetid in _assetid:
        aindex=_assetid.index(assetid)
        assetf=_assetf[aindex]
        assetd=_assetd[aindex]
        assets=_assets[aindex]
        _farmers,_farmernames=contract.functions.viewFarmer().call()
        _distributors,_distributornames=contract.functions.viewDistributor().call()
        _shops,_shopnames=contract.functions.viewShop().call()
        findex=_farmers.index(assetf)
        assetf1=_farmernames[findex]
        if assetf==assetd:
            assetd1="Fake"
        else:
            dindex=_distributors.index(assetd)
            assetd1=_distributornames[dindex]
        if assetf==assets:
            assets1="Fake"
        else:
            sindex=_shops.index(assets)
            assets1=_shopnames[sindex]
    else:
        assetf1="Fake"
        assetd1="Fake"
        assets1="Fake"

    return render_template('index.html',id=assetid,assetf=assetf1,assetd=assetd1,assets=assets1)

@app.route('/farmerdata',methods=['post'])
def farmerdata():
    fwallet=request.form['fwallet']
    fname=request.form['fname']
    print(fwallet,fname)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addFarmer(fwallet,fname).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/farmer')

@app.route('/distributordata',methods=['post'])
def distributordata():
    dwallet=request.form['dwallet']
    dname=request.form['dname']
    print(dwallet,dname)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addDistributor(dwallet,dname).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/distributor')

@app.route('/shopdata',methods=['post'])
def shopdata():
    swallet=request.form['swallet']
    sname=request.form['sname']
    print(swallet,sname)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addShop(swallet,sname).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/shop')

@app.route('/assetdata',methods=['post'])
def assetdata():
    fwallet=request.form['fwallet']
    print(fwallet)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.addAsset(fwallet).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/asset')

@app.route('/sellasset')
def sellasset():
    return render_template('sellasset.html')

@app.route('/sellassettodistributor',methods=['post'])
def sellassettodistributor():
    fwallet=request.form['fwallet']
    dwallet=request.form['dwallet']
    assetid=request.form['assetid']
    print(fwallet,dwallet,assetid)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.sellAssetToDistributor(int(assetid),fwallet,dwallet).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/asset')

@app.route('/sellassettoshop',methods=['post'])
def sellassettoshop():
    dwallet=request.form['dwallet1']
    swallet=request.form['swallet']
    assetid=request.form['assetid1']
    print(swallet,dwallet,assetid)
    contract,web3=connect_with_farmer(0)
    tx_hash=contract.functions.sellAssetToShop(int(assetid),dwallet,swallet).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    return redirect('/asset')

if __name__=="__main__":
    app.run('127.0.0.1',5001,debug=True)