// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FarmTrustProvenance
 * @dev Smart contract for tracking produce from farm to shelf.
 * Each batch of produce is represented as a unique entry with its journey log.
 */
contract FarmTrustProvenance {
    struct ProduceBatch {
        string produceType;
        string farmID;
        uint256 harvestTimestamp;
        string location;
        bool isCertifiedOrganic;
        string[] journeyLog;
    }

    mapping(bytes32 => ProduceBatch) public batches;

    event BatchRegistered(bytes32 indexed batchID, string farmID);
    event JourneyUpdate(bytes32 indexed batchID, string status);

    /**
     * @dev Registers a new produce batch upon harvest.
     */
    function registerBatch(
        bytes32 _batchID,
        string memory _type,
        string memory _farmID,
        bool _isOrganic,
        string memory _location
    ) public {
        ProduceBatch storage batch = batches[_batchID];
        batch.produceType = _type;
        batch.farmID = _farmID;
        batch.harvestTimestamp = block.timestamp;
        batch.isCertifiedOrganic = _isOrganic;
        batch.location = _location;
        
        batch.journeyLog.push(string(abi.encodePacked("Harvested at ", _location)));
        emit BatchRegistered(_batchID, _farmID);
    }

    /**
     * @dev Updates the journey status (e.g., Processed, Shipped, Arrived).
     */
    function updateJourney(bytes32 _batchID, string memory _status) public {
        batches[_batchID].journeyLog.push(_status);
        emit JourneyUpdate(_batchID, _status);
    }

    /**
     * @dev Retrieves the full journey log for a batch.
     */
    function getJourney(bytes32 _batchID) public view returns (string[] memory) {
        return batches[_batchID].journeyLog;
    }

    /**
     * @dev Verifies if a batch is certified organic based on the contract record.
     */
    function verifyOrganicStatus(bytes32 _batchID) public view returns (bool) {
        return batches[_batchID].isCertifiedOrganic;
    }
}
