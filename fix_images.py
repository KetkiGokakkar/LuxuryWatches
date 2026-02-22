import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Watch

artifacts_dir = "/Users/ketkigokakkar/.gemini/antigravity/brain/3af1b4c9-2312-41cf-bfa9-f591b28de9bd/"
media_watches = "/Users/ketkigokakkar/Documents/GitHub/luxurywatch/media/watches/"

submariner_img = [f for f in os.listdir(artifacts_dir) if f.startswith("rolex_submariner")][0]
daytona_img = [f for f in os.listdir(artifacts_dir) if f.startswith("rolex_daytona")][0]
datejust_img = [f for f in os.listdir(artifacts_dir) if f.startswith("rolex_datejust")][0]

shutil.copy(os.path.join(artifacts_dir, submariner_img), os.path.join(media_watches, "fixed_diver.png"))
shutil.copy(os.path.join(artifacts_dir, daytona_img), os.path.join(media_watches, "fixed_chrono.png"))
shutil.copy(os.path.join(artifacts_dir, datejust_img), os.path.join(media_watches, "fixed_dress.png"))

updates = {
    'cartier-santos-medium': "fixed_dress.png",
    'cartier-tank-francaise': "fixed_dress.png",
    'ap-royal-oak-offshore-diver': "fixed_diver.png",
    'audemars-piguet-royal-oak-15500': "fixed_chrono.png",
    'tag-heuer-carrera-chronograph': "fixed_chrono.png"
}

for slug, img in updates.items():
    try:
        w = Watch.objects.get(slug=slug)
        w.image = f'watches/{img}'
        w.save()
        print(f"Fixed image for {slug}")
    except Watch.DoesNotExist:
        print(f"Watch {slug} not found")

