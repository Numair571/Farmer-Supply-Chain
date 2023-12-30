// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract farmer {

  address[] _farmers;
  string[] _farmernames;
  mapping(address=>bool) _f;

  address[] _distributors;
  string[] _distributornames;
  mapping(address=>bool) _d;

  address[] _shops;
  string[] _shopnames;
  mapping(address=>bool) _s;

  uint[] _assetid; 
  address[] _assetf; // producer, madhu (1)
  address[] _assetd; // distributor, madhu (1) -> sindhu (1)
  address[] _assets; // shop, madhu (1) -> sindhu (1) -> krishna (1)

  uint _id;
  address admin;

  constructor() {
    _id=0;
    admin=msg.sender;
  }

  modifier onlyAdmin{
    require(admin==msg.sender);
    _;
  }

  function addFarmer(address fwallet,string memory fname) onlyAdmin public {
      require(!_f[fwallet]);
      _farmers.push(fwallet);
      _farmernames.push(fname);
      _f[fwallet]=true;
  }

  function viewFarmer() public view returns(address[] memory,string[] memory) {
      return(_farmers,_farmernames);
  }

  function addDistributor(address dwallet,string memory dname) onlyAdmin public {
      require(!_d[dwallet]);
      _distributors.push(dwallet);
      _distributornames.push(dname);
      _d[dwallet]=true;
  }

  function viewDistributor() public view returns(address[] memory,string[] memory) {
      return(_distributors,_distributornames);
  }

  function addShop(address swallet,string memory sname) onlyAdmin public {
      require(!_s[swallet]);
      _shops.push(swallet);
      _shopnames.push(sname);
      _s[swallet]=true;
  }

  function viewShop() public view returns(address[] memory,string[] memory) {
      return(_shops,_shopnames);
  }

  function addAsset(address fwallet) public {
      require(_f[fwallet]);
      _id+=1;
      _assetid.push(_id);
      _assetf.push(fwallet);
      _assetd.push(fwallet); // dwallet
      _assets.push(fwallet); // swallet
  }

  function viewAsset() public view returns(uint[] memory,address[] memory,address[] memory,address[] memory) {
      return(_assetid,_assetf,_assetd,_assets);
  }

  function sellAssetToDistributor(uint assetid,address fwallet,address dwallet) public returns(bool) {
      
      uint i; // 1, madhu(f), madhu(d), madhu(s)
      require(_f[fwallet]); //1, madhu(f), sindhu (d)
      require(_d[dwallet]);

      for(i=0;i<_assetid.length;i++){
        if(_assetid[i]==assetid && _assetf[i]==fwallet){ // 1==1 && madhu==madhu
          _assetd[i]=dwallet; // 1, madhu(f), sindhu(d), madhu(s)
          return true;
        }
      }

      return false;
  }

  function sellAssetToShop(uint assetid,address dwallet,address swallet) public returns(bool){
      uint i;

      require(_d[dwallet]); // 1, madhu(f), sindhu(d),madhu(s)
      require(_s[swallet]);

      for(i=0;i<_assetid.length;i++){
        if(_assetid[i]==assetid && _assetd[i]==dwallet){ // 1==1 && sindhu==sindhu
          _assets[i]=swallet; // 1, madhu(f), sindhu(d), krishna(s)
          return true;
        }
      }
      return false;
  }
}
