// SPDX-License-Identifier: Unlicensed

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 favoritenumber;

    function store(uint256 _favoritenumber) public returns (uint256) {
        favoritenumber = _favoritenumber;
        return _favoritenumber;
    }

    function retrieve() public view returns (uint256) {
        return favoritenumber;
    }

    /*
      uint256 favoritenumber2;
      
      function store2(uint256 _favoritenumber2) public{
          favoritenumber2 = _favoritenumber2;
      }
        function retrieve2() public view returns(uint256){
            return favoritenumber2;
        }
            uint256 favoritesoma;
/*
/*
      function soma() public{
          favoritesoma = favoritenumber + favoritenumber2;
      }
      function returnsoma() public view returns(uint256){
 
          return favoritesoma;
      }
*/
    struct People {
        uint256 favoritenumber;
        string name;
    }
    bool favoritebool;

    People[] public people; // se colocar algum numero dentro do Array, irei limitar ele a esse numero
    //people public person = people({favoritesoma:100, name:"Patricia"});
    mapping(string => uint256) public nametofavoritenumber;

    function addperson(string memory _name, uint256 _favoritenumber) public {
        people.push(People(_favoritenumber, _name));
        nametofavoritenumber[_name] = _favoritenumber;
    } // we can store things in "memory" or in "storage".
    //Memory means that after this exection it will leave it; Storage will keep it forever
}
