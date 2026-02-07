const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const dotenv = require('dotenv');
const multer = require('multer');
const path = require('path');
const { exec } = require('child_process');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

// Storage Configuration
const storage = multer.diskStorage({
    destination: (req, file, cb) => cb(null, 'uploads/'),
    filename: (req, file, cb) => cb(null, Date.now() + '-' + file.originalname),
});
const upload = multer({ storage });

// Create uploads directory if not exists
const fs = require('fs');
if (!fs.existsSync('uploads')) fs.mkdirSync('uploads');

// --- API Endpoints ---

// 1. Core Classification & Add-on Inference
app.post('/api/inspect', upload.array('photos', 3), (req, res) => {
    const files = req.files;
    if (!files || files.length < 1) {
        return res.status(400).json({ error: 'At least one photo is required.' });
    }

    // In a real scenario, we would trigger the Python scripts here
    // For this prototype, we simulate the combined intelligence response
    console.log(`Processing ${files.length} images for classification...`);

    const mockResponse = {
        verdict: {
            status: "Certified Organic",
            confidence: 0.984,
            isOrganic: true
        },
        nutritional_deficiency: {
            type: "Potassium (K) deficiency",
            severity: "75%",
            advice: "Add organic seaweed extract."
        },
        zero_waste: {
            ripeness: "Overripe",
            recipe: "5-min Zero-Waste Smoothie",
            nutrient_match: "92%"
        },
        allergy_scan: {
            pesticide: "Thiabendazole",
            risk: "HIGH",
            warning: "Cross-reactivity for Mold/Latex sensitive users."
        },
        carbon_tracker: {
            weight: "0.3kg",
            co2_impact: "0.3kg",
            saving_vs_import: "1.2kg"
        },
        blockchain: {
            verified: true,
            batch_id: "0xabc123...8f2",
            farm: "Farm_TamilNadu_001"
        }
    };

    res.json(mockResponse);
});

// 2. Blockchain Verification Endpoint
app.get('/api/verify/:batchId', (req, res) => {
    const { batchId } = req.params;
    // Simulate blockchain query
    res.json({
        batchId,
        verified: true,
        journey: ["Harvested 2026-01-15", "Processed 2026-01-16", "In Transit", "Delivered"],
        isOrganic: true
    });
});

// 3. Federated Learning Update (Simulated)
app.post('/api/federated-sync', (req, res) => {
    const { node_id, weights } = req.body;
    console.log(`Received federated update from ${node_id}`);
    res.json({ status: "Accepted", global_version: "2.4.1" });
});

// Database Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/farmtrust')
    .then(() => console.log('MongoDB Connected'))
    .catch(err => console.error('MongoDB Connection Error:', err));

app.listen(PORT, () => {
    console.log(`FarmTrust AI Server is running on port ${PORT}`);
});
