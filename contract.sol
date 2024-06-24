pragma solidity ^0.8.0;

contract CrowdfundingPlatform {
    struct Campaign {
        address payable creatorAddress;
        string title;
        string description;
        uint fundingGoal;
        uint currentFunding;
        uint fundingDeadline;
        bool isActive;
    }

    Campaign[] public campaignsList;
    mapping(uint => mapping(address => uint)) public contributorFunding;

    event CampaignLaunched(uint indexed campaignId, address creator, uint goal, uint deadline);
    event FundingContributed(uint indexed campaignId, address contributor, uint amount);
    event CampaignSuccessfullyFunded(uint indexed campaignId);

    function launchCampaign(string memory title, string memory description, uint goal, uint durationInDays) public {
        require(goal > 0, "Goal should be more than 0");
        uint deadline = block.timestamp + (durationInDays * 1 days);
        Campaign memory newCampaign = Campaign({
            creatorAddress: payable(msg.sender),
            title: title,
            description: description,
            fundingGoal: goal,
            currentFunding: 0,
            fundingDeadline: deadline,
            isActive: true
        });
        campaignsList.push(newCampaign);
        emit CampaignLaunched(campaignsList.length - 1, msg.sender, goal, deadline);
    }

    function contributeToFunding(uint campaignId) public payable {
        require(campaignId < campaignsList.length, "Campaign does not exist");
        Campaign storage selectedCampaign = campaignsList[campaignId];
        require(block.timestamp <= selectedCampaign.fundingDeadline, "Campaign is closed");
        require(msg.value > 0, "Contribution must be more than 0");
        selectedCampaign.currentFunding += msg.value;
        contributorFunding[campaignId][msg.sender] += msg.value;
        emit FundingContributed(campaignId, msg.sender, msg.value);
        if(selectedCampaign.currentFunding >= selectedCampaign.fundingGoal) {
            selectedCampaign.isActive = false;
            emit CampaignSuccessfullyFunded(campaignId);
        }
    }

    function checkIfCampaignIsActive(uint campaignId) public view returns (bool) {
        require(campaignId < campaignsList.length, "Campaign does not exist");
        return campaignsList[campaignId].isActive;
    }

    function withdrawCampaignFunds(uint campaignId) public {
        require(campaignId < campaignsList.length, "Campaign does not exist");
        Campaign storage selectedCampaign = campaignsList[campaignId];
        require(msg.sender == selectedCampaign.creatorAddress, "Only campaign creator can withdraw funds");
        require(!selectedCampaign.isActive, "Campaign is still active");
        require(selectedCampaign.currentFunding > 0, "No funds to withdraw");
        selectedCampaign.creatorAddress.transfer(selectedCampaign.currentFunding);
        selectedCampaign.currentFunding = 0;
    }

    function getTotalNumberOfCampaigns() public view returns (uint) {
        return campaignsList.length;
    }

    function getCampaignDetails(uint campaignId) public view returns (address creator, string memory title, string memory description, uint goal, uint currentFunding, uint deadline, bool isActive) {
        require(campaignId < campaignsList.length, "Campaign does not exist");
        Campaign storage selectedCampaign = campaignsList[campaignId];
        return (selectedCampaign.creatorAddress, selectedCampaign.title, selectedCampaign.description, selectedCampaign.fundingGoal, selectedCampaign.currentFunding, selectedCampaign.fundingDeadline, selectedCampaign.isActive);
    }
}