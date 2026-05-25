from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session
from app import schemas , models
from app.database import get_db

router = APIRouter()

def calculate_bmi(weight_kg: float , height_cm:float) -> float:
    height_m = height_cm / 100
    return round(weight_kg/ (height_m ** 2), 2)

def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    elif bmi <25:
        return "normal"
    elif bmi < 30:
        return "overweight"
    else :
        return "obese"
    
def calculate_daily_calories(
    weight_kg: float,
    height_cm:float,
    age: int,
    gender: str,
    activity_level: str
) -> float:
    if gender.lower() == "male":
        bmr = 88.36 + (13.4 * weight_kg) + (4.8 * height_cm) - (5.7 * age)
    else :
        bmr = 447.6 + (9.2 * weight_kg) + (3.1 * height_cm) - (4.3 * age)
    
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return round(bmr * multipliers.get(activity_level , 1.2), 2)

MEAL_PLANS = {
    "weight_loss": {
        "breakfast": "Oats with skimmed milk, 2 boiled eggs, 1 fruit (apple or banana)",
        "lunch": "Grilled chicken breast, steamed vegetables (broccoli, carrots), small bowl of brown rice",
        "dinner": "Vegetable soup, 2 egg whites, cucumber salad",
        "snacks": "Greek yogurt, handful of almonds, fish oil (omega-3) supplement",
        "protein_g": 140,
        "carbs_g": 150,
        "fat_g": 40
    },
    "weight_gain": {
        "breakfast": "4 whole eggs, 2 slices whole grain bread, banana, full fat milk",
        "lunch": "Rice (chawal), dal (lentils), paneer or chicken curry, curd",
        "dinner": "Roti with sabzi, chicken or paneer, glass of whole milk",
        "snacks": "Peanut butter with banana, mixed nuts (badam, kaju, akhrot), fish oil (omega-3) supplement",
        "protein_g": 150,
        "carbs_g": 300,
        "fat_g": 80
    },
    "muscle_building": {
        "breakfast": "6 egg whites + 1 whole egg omelette, oats (complex carbs for pre-workout energy), black coffee",
        "lunch": "Grilled chicken breast, brown rice (complex carbs - chawal with husk), steamed broccoli",
        "dinner": "Paneer or chicken, sauteed vegetables, small portion of sweet potato (shakarkand)",
        "snacks": "Whey protein shake post-workout, handful of almonds, fish oil (omega-3) + multivitamin tablet",
        "protein_g": 180,
        "carbs_g": 200,
        "fat_g": 50
    },
    "balanced": {
        "breakfast": "2 eggs any style, 1 bowl oats or upma, 1 seasonal fruit",
        "lunch": "Dal (legumes - rajma, chana, moong), roti or rice, mixed vegetable sabzi, curd",
        "dinner": "Grilled fish or paneer, 2 rotis, salad with olive oil dressing",
        "snacks": "Fruit chaat, roasted chana, fish oil (omega-3) + multivitamin tablet",
        "protein_g": 120,
        "carbs_g": 220,
        "fat_g": 55
    },
    "diabetes": {
        "breakfast": "2 boiled eggs, vegetable upma (small portion), cucumber slices, green tea",
        "lunch": "Moong dal (low glycemic legumes), 1-2 roti (whole wheat), bitter gourd (karela) sabzi, small bowl curd",
        "dinner": "Grilled chicken or fish, steamed vegetables (no potato), small bowl of brown rice",
        "snacks": "Handful of walnuts (akhrot), buttermilk (chaas), small apple or pear"
    }
}

@router.get("/{user_id}", response_model=schemas.DietRecommendation)
def get_recommendation(user_id:int, db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user :
        raise HTTPException(status_code=404 , detail="User not found")
    
    bmi = calculate_bmi(user.weight_kg , user.height_cm)
    bmi_category = get_bmi_category(bmi)
    daily_calories = calculate_daily_calories(
        user.weight_kg,
        user.height_cm,
        user.age,
        user.gender,
        user.activity_level
    )
    plan = MEAL_PLANS[user.health_goal]
    
    return schemas.DietRecommendation(
        user_id= user.id,
        bmi=bmi,
        bmi_category= bmi_category,
        daily_calorie=daily_calories,
        diet_category=user.health_goal,
        breakfast=plan["breakfast"],
        lunch = plan["lunch"],
        dinner= plan["dinner"],
        snacks= plan.get("snacks", "No snacks specified"),
        protein_g=plan.get("protein_g", 0),
        carbs_g= plan.get("carbs_g", 0),
        fat_g=plan.get("fat_g", 0)     
    )