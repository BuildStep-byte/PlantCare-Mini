import pandas as pd
from datetime import datetime

# Читаем данные
df = pd.read_csv('plants.csv')

# Превращаем колонку с датой в формат даты
df['last_watered'] = pd.to_datetime(df['last_watered'])

# Считаем дату следующего полива
df['next_watering'] = df['last_watered'] + pd.to_timedelta(df['interval_days'], unit='D')

# Сегодняшняя дата
today = pd.Timestamp.now().normalize()

# Добавляем колонку «дней до полива»
df['days_until'] = (df['next_watering'] - today).dt.days

# Сортируем по сроку: сначала те, у кого меньше дней
df_sorted = df.sort_values(by='days_until')

print("=== План полива ===")
for _, row in df_sorted.iterrows():
    name = row['name']
    next_date = row['next_watering'].strftime('%Y-%m-%d')
    days = row['days_until']

    if days < 0:
        status = "⚠️ Просрочен!"
    elif days == 0:
        status = "🌱 Пора сегодня!"
    elif days <= 3:
        status = f"🌱 Скоро (через {days} дн.)"
    else:
        status = f"⏳ Пока спокойно ({days} дн.)"

    print(f"{status} | {name} — следующий полив: {next_date}")

print("\n=== Полная таблица (для проверки) ===")
print(df[['name', 'last_watered', 'next_watering', 'days_until']].to_string(index=False))