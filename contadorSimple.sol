// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Contador {
    uint256 private contador;
    address public owner;
    mapping(address => bool) public whitelist;

    event ContadorModificado(address indexed modificadaPor, uint256 nuevoValor);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Solo el propietario puede realizar esta accion");
        _;
    }

    modifier onlyWhitelisted() {
        require(whitelist[msg.sender], "No estas en la whitelist");
        _;
    }

    function incrementarContador(uint256 cantidad) public onlyWhitelisted {
        contador += cantidad;
        emit ContadorModificado(msg.sender, contador);
    }

    function decrementarContador(uint256 cantidad) public onlyWhitelisted {
        require(contador >= cantidad, "No se puede decrementar por debajo de cero");
        contador -= cantidad;
        emit ContadorModificado(msg.sender, contador);
    }

    function obtenerContador() public view returns (uint256) {
        return contador;
    }

    function AddToWhitelist(address cuenta) public onlyOwner {
        whitelist[cuenta] = true;
    }

    function removeFromWhitelist(address cuenta) public onlyOwner {
        whitelist[cuenta] = false;
    }
}
