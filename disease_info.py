"""Human-readable plant + disease metadata for predictions.

Keys are the PlantVillage class folder names. Each entry has:
  plant: common plant name
  condition: 'Healthy' or disease name
  status: 'healthy' | 'diseased'
  description: short description
  treatment: recommended action (or '' for healthy plants)
"""

DISEASE_INFO = {
    "Apple___Apple_scab": {
        "plant": "Apple", "condition": "Apple scab", "status": "diseased",
        "description": "Fungal disease (Venturia inaequalis) causing olive-green to brown lesions on leaves and fruit.",
        "treatment": "Apply fungicides at green-tip stage; prune for airflow; remove fallen leaves to reduce inoculum.",
    },
    "Apple___Black_rot": {
        "plant": "Apple", "condition": "Black rot", "status": "diseased",
        "description": "Fungal disease (Botryosphaeria obtusa) producing purple leaf spots and rotting fruit.",
        "treatment": "Prune out cankers and mummified fruit; apply protective fungicides during bloom.",
    },
    "Apple___Cedar_apple_rust": {
        "plant": "Apple", "condition": "Cedar apple rust", "status": "diseased",
        "description": "Fungal disease (Gymnosporangium juniperi-virginianae) showing bright orange-yellow leaf spots.",
        "treatment": "Remove nearby junipers if possible; apply fungicide from pink stage through petal fall.",
    },
    "Apple___healthy": {
        "plant": "Apple", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Blueberry___healthy": {
        "plant": "Blueberry", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "plant": "Cherry", "condition": "Powdery mildew", "status": "diseased",
        "description": "Fungal disease (Podosphaera clandestina) producing white powdery growth on leaves and shoots.",
        "treatment": "Apply sulfur or other fungicides; prune for ventilation; avoid excess nitrogen.",
    },
    "Cherry_(including_sour)___healthy": {
        "plant": "Cherry", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "plant": "Corn", "condition": "Gray leaf spot", "status": "diseased",
        "description": "Fungal disease (Cercospora zeae-maydis) producing rectangular gray-brown lesions on leaves.",
        "treatment": "Rotate crops; use resistant hybrids; apply fungicides at tasseling if pressure is high.",
    },
    "Corn_(maize)___Common_rust_": {
        "plant": "Corn", "condition": "Common rust", "status": "diseased",
        "description": "Fungal disease (Puccinia sorghi) causing reddish-brown pustules on both leaf surfaces.",
        "treatment": "Plant resistant hybrids; apply fungicides early in severe outbreaks.",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "plant": "Corn", "condition": "Northern leaf blight", "status": "diseased",
        "description": "Fungal disease (Exserohilum turcicum) causing long elliptical gray-green lesions on leaves.",
        "treatment": "Use resistant hybrids; rotate crops; apply foliar fungicides at tasseling.",
    },
    "Corn_(maize)___healthy": {
        "plant": "Corn", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Grape___Black_rot": {
        "plant": "Grape", "condition": "Black rot", "status": "diseased",
        "description": "Fungal disease (Guignardia bidwellii) causing brown leaf lesions and shriveled black berries.",
        "treatment": "Remove mummified fruit; apply fungicides from bud break through veraison.",
    },
    "Grape___Esca_(Black_Measles)": {
        "plant": "Grape", "condition": "Esca (Black Measles)", "status": "diseased",
        "description": "Trunk-disease complex causing tiger-stripe leaf patterns and dark berry spotting.",
        "treatment": "Prune out infected wood; protect pruning wounds; remove severely affected vines.",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "plant": "Grape", "condition": "Leaf blight (Isariopsis)", "status": "diseased",
        "description": "Fungal disease causing irregular dark brown leaf spots, often late in the season.",
        "treatment": "Apply protective fungicides; improve canopy airflow; remove infected leaves.",
    },
    "Grape___healthy": {
        "plant": "Grape", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "plant": "Orange", "condition": "Citrus greening (HLB)", "status": "diseased",
        "description": "Bacterial disease spread by psyllids; causes blotchy mottle and lopsided bitter fruit.",
        "treatment": "Remove infected trees; control psyllid vector; use certified disease-free planting material.",
    },
    "Peach___Bacterial_spot": {
        "plant": "Peach", "condition": "Bacterial spot", "status": "diseased",
        "description": "Bacterial disease (Xanthomonas) causing small dark angular leaf spots and fruit pitting.",
        "treatment": "Plant resistant cultivars; apply copper sprays; avoid overhead irrigation.",
    },
    "Peach___healthy": {
        "plant": "Peach", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Pepper,_bell___Bacterial_spot": {
        "plant": "Bell pepper", "condition": "Bacterial spot", "status": "diseased",
        "description": "Bacterial disease (Xanthomonas) causing water-soaked leaf lesions that turn brown.",
        "treatment": "Use disease-free seed; apply copper-based bactericides; avoid working plants when wet.",
    },
    "Pepper,_bell___healthy": {
        "plant": "Bell pepper", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Potato___Early_blight": {
        "plant": "Potato", "condition": "Early blight", "status": "diseased",
        "description": "Fungal disease (Alternaria solani) causing concentric-ring brown lesions on older leaves.",
        "treatment": "Rotate crops; maintain plant vigor; apply fungicides like chlorothalonil or mancozeb.",
    },
    "Potato___Late_blight": {
        "plant": "Potato", "condition": "Late blight", "status": "diseased",
        "description": "Oomycete disease (Phytophthora infestans) causing rapidly spreading water-soaked lesions.",
        "treatment": "Destroy infected plants; apply preventive fungicides; avoid overhead watering.",
    },
    "Potato___healthy": {
        "plant": "Potato", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Raspberry___healthy": {
        "plant": "Raspberry", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Soybean___healthy": {
        "plant": "Soybean", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Squash___Powdery_mildew": {
        "plant": "Squash", "condition": "Powdery mildew", "status": "diseased",
        "description": "Fungal disease producing white powdery patches on leaves and stems.",
        "treatment": "Apply sulfur, potassium bicarbonate, or neem-based fungicides; improve airflow.",
    },
    "Strawberry___Leaf_scorch": {
        "plant": "Strawberry", "condition": "Leaf scorch", "status": "diseased",
        "description": "Fungal disease (Diplocarpon earliana) causing purple leaf spots that merge and scorch.",
        "treatment": "Remove infected leaves; rotate beds; apply fungicides preventively in spring.",
    },
    "Strawberry___healthy": {
        "plant": "Strawberry", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Tomato___Bacterial_spot": {
        "plant": "Tomato", "condition": "Bacterial spot", "status": "diseased",
        "description": "Bacterial disease (Xanthomonas) causing small dark leaf spots and fruit lesions.",
        "treatment": "Use certified seed; apply copper sprays; avoid overhead irrigation.",
    },
    "Tomato___Early_blight": {
        "plant": "Tomato", "condition": "Early blight", "status": "diseased",
        "description": "Fungal disease (Alternaria solani) causing target-like brown spots on lower leaves.",
        "treatment": "Mulch to prevent splash; rotate crops; apply chlorothalonil or copper fungicides.",
    },
    "Tomato___Late_blight": {
        "plant": "Tomato", "condition": "Late blight", "status": "diseased",
        "description": "Oomycete disease (Phytophthora infestans) causing greasy gray-green leaf lesions.",
        "treatment": "Remove infected plants immediately; apply preventive fungicides; avoid wet foliage.",
    },
    "Tomato___Leaf_Mold": {
        "plant": "Tomato", "condition": "Leaf mold", "status": "diseased",
        "description": "Fungal disease (Passalora fulva) causing yellow leaf spots with olive mold beneath.",
        "treatment": "Improve ventilation in greenhouses; reduce humidity; apply fungicides if needed.",
    },
    "Tomato___Septoria_leaf_spot": {
        "plant": "Tomato", "condition": "Septoria leaf spot", "status": "diseased",
        "description": "Fungal disease (Septoria lycopersici) causing many small circular spots with dark borders.",
        "treatment": "Remove infected leaves; mulch; apply chlorothalonil or copper fungicides.",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "plant": "Tomato", "condition": "Two-spotted spider mite", "status": "diseased",
        "description": "Mite infestation (Tetranychus urticae) causing fine stippling, bronzing, and webbing.",
        "treatment": "Spray water to dislodge mites; use insecticidal soap or miticides; encourage predators.",
    },
    "Tomato___Target_Spot": {
        "plant": "Tomato", "condition": "Target spot", "status": "diseased",
        "description": "Fungal disease (Corynespora cassiicola) producing concentric ring lesions on leaves and fruit.",
        "treatment": "Improve airflow; remove infected debris; apply broad-spectrum fungicides.",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "plant": "Tomato", "condition": "Yellow leaf curl virus", "status": "diseased",
        "description": "Viral disease spread by whiteflies; causes upward curling, yellowing, and stunting.",
        "treatment": "Control whiteflies with insecticides or row covers; remove infected plants; use resistant varieties.",
    },
    "Tomato___Tomato_mosaic_virus": {
        "plant": "Tomato", "condition": "Mosaic virus", "status": "diseased",
        "description": "Viral disease producing mottled light/dark green leaves and distorted growth.",
        "treatment": "Remove and destroy infected plants; sanitize tools; plant resistant cultivars.",
    },
    "Tomato___healthy": {
        "plant": "Tomato", "condition": "Healthy", "status": "healthy",
        "description": "Leaf shows no signs of disease.",
        "treatment": "",
    },
    "Background_without_leaves": {
        "plant": "—", "condition": "No leaf detected", "status": "unknown",
        "description": "Image does not appear to contain a plant leaf.",
        "treatment": "",
    },
}


def lookup(class_name):
    if class_name in DISEASE_INFO:
        return DISEASE_INFO[class_name]
    plant, _, condition = class_name.partition("___")
    return {
        "plant": plant.replace("_", " ").strip() or "Unknown",
        "condition": condition.replace("_", " ").strip() or class_name,
        "status": "healthy" if "healthy" in class_name.lower() else "diseased",
        "description": "",
        "treatment": "",
    }
