# PlantDoc — CNN Plant Disease Web App

A Flask web app that diagnoses plant diseases from leaf images using the
exact CNN methodology described in the Sem 5 project notebook and research paper.

> **Note:** the trained model file (`model/*.h5`) is gitignored to keep the
> repo lightweight. Run `python train.py` (step 2 below) to generate it on
> your machine before starting the app.

## Methodology (matches the source notebook)

- **Input:** 128 × 128 RGB images, normalized to `[0, 1]`
- **Architecture:**
  ```
  Conv2D(32, 3×3, ReLU) → MaxPool(2×2)
  Conv2D(64, 3×3, ReLU) → MaxPool(2×2)
  Conv2D(128, 3×3, ReLU) → MaxPool(2×2)
  Flatten → Dense(128, ReLU) → Dropout(0.5) → Dense(N, Softmax)
  ```
- **Loss / optimizer:** categorical cross-entropy + Adam
- **Augmentation:** rotation, zoom, width/height shift, shear, horizontal flip
- **Split:** 80 / 20 train / test, `random_state=42`
- **Training:** 20 epochs, batch size 32

## Project layout

```
plant_disease_webapp/
├── app.py                # Flask backend
├── train.py              # Trains the CNN, saves model + class names
├── disease_info.py       # Plant/disease metadata (descriptions + treatments)
├── requirements.txt
├── templates/index.html  # UI
├── static/style.css
├── static/script.js
└── model/                # Populated by train.py
    ├── plant_disease_model.h5
    ├── class_names.json
    └── history.json
```

## 1. Install

```bash
cd /Users/bhaau/plant_disease_webapp
pip install -r requirements.txt
```

## 2. Train the model

The training script expects the PlantVillage dataset arranged as one folder per class.
A copy is already present at `/Users/bhaau/PlantVillage-Dataset/raw/color`.

```bash
# Full training (38 classes, ~54k images)
python train.py --data-dir /Users/bhaau/PlantVillage-Dataset/raw/color

# Fast smoke test (cap images per class)
python train.py --data-dir /Users/bhaau/PlantVillage-Dataset/raw/color --max-per-class 50 --epochs 5
```

Outputs land in `model/`:
- `plant_disease_model.h5` — Keras model
- `class_names.json` — class index → label mapping
- `history.json` — per-epoch accuracy / loss

## 3. Run the web app

```bash
python app.py
# open http://localhost:5000
```

Drag-and-drop a leaf image into the page; the app returns the top prediction
(plant + disease + confidence) plus the next four candidates.

## API

| Method | Path           | Purpose                                |
|--------|----------------|----------------------------------------|
| GET    | `/`            | UI                                     |
| GET    | `/api/health`  | Liveness + model-loaded flag           |
| GET    | `/api/info`    | Class list + training history          |
| POST   | `/api/predict` | Multipart `image` field → predictions  |

Sample call:
```bash
curl -F "image=@leaf.jpg" http://localhost:5000/api/predict
```
