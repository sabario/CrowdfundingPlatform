pragma solidity ^0.8.0;

contract CrowdfundingPlatform {
    struct Campaign {
        address payable creator;
        string title;
        string description;
        uint goal;
        uint funds;
        uint deadline;
        bool isOpen;
    }

    Campaign[] public campaigns;
    mapping(uint => mapping(address => uint)) public contributions;

    event CampaignCreated(uint indexed campaignId, address creator, uint goal, uint deadline);
    event ContributionMade(uint indexed campaignId, address contributor, uint amount);
    event CampaignFunded(uint indexed campaignId);

    function createCampaign(string memory title, string memory description, uint goal, uint durationInDays) public {
        require(goal > 0, "Goal should be more than 0");
        uint deadline = block.timestamp + (durationInDays * 1 days);
        Campaign memory newCampaign = Campaign({
            creator: payable(msg.sender),
            title: title,
            description: description,
            goal: goal,
            funds: 0,
            deadline: deadline,
            isOpen: true
        });
        campaigns.push(newCampaign);
        emit CampaignCreated(campaigns.length - 1, msg.sender, goal, deadline);
    }

    function contribute(uint campaignId) public payable {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage campaign = campaigns[campaignId];
        require(block.timestamp <= campaign.deadline, "Campaign is closed");
        require(msg.value > 0, "Contribution must be more than 0");
        campaign.funds += msg.value;
        contributions[campaignId][msg.sender] += msg.value;
        emit ContributionMade(campaignId, msg.sender, msg.value);
        if(campaign.funds >= campaign.goal) {
            campaign.isOpen = false;
            emit CampaignFunded(campaignId);
        }
    }

    function isCampaignOpen(uint campaignId) public view returns (bool) {
        require(campaignId < campaigns.length, "Campaign does not exist");
        return campaigns[campaignId].isOpen;
    }

    function withdrawFunds(uint campaignId) public {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage campaign = campaigns[campaignId];
        require(msg.sender == campaign.creator, "Only campaign creator can withdraw funds");
        require(!campaign.isOpen, "Campaign is still open");
        require(campaign.funds > 0, "No funds to withdraw");
        campaign.creator.transfer(campaign.funds);
        campaign.funds = 0;
    }

    function getNumberOfCampaigns() public view returns (uint) {
        return campaigns.length;
    }

    function getCampaign(uint campaignId) public view returns (address creator, string memory title, string memory description, uint goal, uint funds, uint deadline, bool isOpen) {
        require(campaignId < campaigns.length, "Campaign does not exist");
        Campaign storage campaign = campaigns[campaignId];
        return (campaign.creator, campaign.title, campaign.description, campaign.goal, campaign.funds, campaign.deadline, campaign.isOpen);
    }
}