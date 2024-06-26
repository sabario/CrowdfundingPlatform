pragma solidity ^0.8.0;

contract CrowdfundingPlatform {
    struct Campaign {
        address payable creator;
        string title;
        string description;
        uint goalAmount;
        uint fundedAmount;
        uint endTimestamp;
        bool isOpen;
    }

    Campaign[] public campaigns;
    mapping(uint => mapping(address => uint)) public contributions;

    event CampaignCreated(uint indexed campaignId, address creator, uint goal, uint deadline);
    event ContributionMade(uint indexed campaignId, address contributor, uint amount);
    event CampaignFunded(uint indexed campaignId);

    function createCampaign(string memory title, string memory description, uint goal, uint durationDays) public {
        require(goal > 0, "Goal must exceed 0");
        uint deadline = block.timestamp + (durationDays * 1 days);
        Campaign memory newCampaign = Campaign({
            creator: payable(msg.sender),
            title: title,
            description: description,
            goalAmount: goal,
            fundedAmount: 0,
            endTimestamp: deadline,
            isOpen: true
        });
        campaigns.push(newCampaign);
        emit CampaignCreated(campaigns.length - 1, msg.sender, goal, deadline);
    }

    function contribute(uint campaignId) public payable {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage targetCampaign = campaigns[campaignId];
        require(block.timestamp <= targetCampaign.endTimestamp, "Campaign is closed");
        require(msg.value > 0, "Contribution must exceed 0");
        targetCampaign.fundedAmount += msg.value;
        contributions[campaignId][msg.sender] += msg.value;
        emit ContributionMade(campaignId, msg.sender, msg.value);
        if(targetCampaign.fundedArray >= targetCampaign.goalAmount) {
            targetCampaign.isOpen = false;
            emit CampaignFunded(campaignId);
        }
    }

    function isCampaignOpen(uint campaignId) public view returns (bool) {
        require(campaignId < campaigns.length, "Campaign does not exist");
        return campaigns[campaignId].isOpen;
    }

    function withdrawFunds(uint campaignId) public {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage targetCampaign = campaigns[campaignId];
        require(msg.sender == targetCampaign.creator, "Withdrawal permitted to creator only");
        require(!targetCampaign.isOpen, "Campaign is still open");
        require(targetCampaign.fundedAmount > 0, "No funds available");
        targetCampaign.creator.transfer(targetCampaign.fundedAmount);
        targetCampaign.fundedAmount = 0;
    }

    function getCampaignsCount() public view returns (uint) {
        return campaigns.length;
    }

    function getCampaign(uint campaignId) public view returns (address creator, string memory title, string memory description, uint goal, uint fundedAmount, uint deadline, bool isOpen) {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage targetCampaign = campaigns[campaignId];
        return (targetCampaign.creator, targetCampaign.title, targetCampaign.description, targetCampaign.goalAmount, targetCampaign.fundedAmount, targetCampaign.endTimestamp, targetCampaign.isOpen);
    }
}