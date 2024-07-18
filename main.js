import Web3 from 'web3';
import axios from 'axios';
import { CONTRACT_ADDRESS, ABI, API_ENDPOINT } from './config';

if (typeof window.ethereum !== 'undefined') {
    window.web3 = new Web3(window.ethereum);
} else {
    console.error('MetaMask is not installed. Please install MetaMask to use this platform.');
}

async function connectWallet() {
    try {
        await window.ethereum.request({ method: 'eth_requestAccounts' });
        console.log('Connected to the wallet successfully.');
    } catch (error) {
        console.error('Error connecting to the wallet:', error);
    }
}

const contract = new window.web3.eth.Contract(ABI, CONTRACT_ADDRESS);

const cache = new Map();

async function fetchCampaigns() {
    const cacheKey = 'campaigns';
    if (cache.has(cacheKey)) {
        return cache.get(cacheKey);
    }

    try {
        const response = await axios.get(`${API_ENDPOINT}/campaigns`);
        const data = response.data;
        cache.set(cacheKey, data);
        return data;
    } catch (error) {
        console.error('Error fetching campaigns:', error);
        return [];
    }
}

function displayCampaigns(campaigns) {
    const campaignsContainer = document.getElementById('campaignsContainer');
    campaignsContainer.innerHTML = '';

    campaigns.forEach(campaign => {
        const campaignElement = document.createElement('div');
        campaignElement.innerHTML = `
            <h3>${campaign.title}</h3>
            <p>${campaign.description}</p>
            <p>Goal: ${campaign.goal}</p>
            <button onclick="handleContribute('${campaign.id}', '0.1')">Contribute 0.1 ETH</button>
        `;
        campaignsContainer.appendChild(campaignElement);
    });
}

async function getAccounts() {
    const cacheKey = 'accounts';
    if (cache.has(cacheKey)) {
        return cache.get(cacheKey);
    }

    const accounts = await window.web3.eth.getAccounts();
    cache.set(cacheKey, accounts);
    return accounts;
}

async function handleContribute(campaignId, amount) {
    const accounts = await getAccounts();
    if (accounts.length === 0) {
        console.warn('Please connect your wallet to contribute.');
        return;
    }

    const amountInWei = window.web3.utils.toWei(amount, 'ether');
    try {
        await contract.methods.contributeToCampaign(campaignId).send({ from: accounts[0], value: amountInWei });
        console.log('Contribution successful');
    } catch (error) {
        console.error('Error contributing:', error);
    }
}

function setupEventListeners() {
    document.getElementById('connectWalletBtn').addEventListener('click', connectWallet);

    document.addEventListener('DOMContentLoaded', async () => {
        const campaigns = await fetchCampaigns();
        displayCampaigns(campaigns);
    });
}

async function init() {
    setupEventListeners();
}

init();