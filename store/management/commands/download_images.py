import os
import urllib.request
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from store.models import Watch


class Command(BaseCommand):
    help = 'Downloads high-quality watch images and assigns them to watches'

    def handle(self, *args, **options):
        # High-quality watch images from Unsplash (free to use)
        watch_images = {
            'rolex-submariner-date-41': [
                'https://images.unsplash.com/photo-1622434641406-a158123450f9?w=800&q=90',
            ],
            'rolex-daytona-cosmograph': [
                'https://images.unsplash.com/photo-1548171915-e79a380a2a4b?w=800&q=90',
            ],
            'rolex-datejust-36': [
                'https://images.unsplash.com/photo-1627037558426-c2d07beda3af?w=800&q=90',
            ],
            'patek-philippe-nautilus-5711': [
                'https://images.unsplash.com/photo-1594534475808-b18fc33b045e?w=800&q=90',
            ],
            'patek-philippe-calatrava-5227r': [
                'https://images.unsplash.com/photo-1612817159949-195b6eb9e31a?w=800&q=90',
            ],
            'audemars-piguet-royal-oak-15500': [
                'https://images.unsplash.com/photo-1618220179428-22790b461013?w=800&q=90',
            ],
            'omega-speedmaster-moonwatch': [
                'https://images.unsplash.com/photo-1614164185128-e4ec99c436d7?w=800&q=90',
            ],
            'omega-seamaster-planet-ocean': [
                'https://images.unsplash.com/photo-1585123334904-845d60e97b29?w=800&q=90',
            ],
            'tag-heuer-monaco-heuer-02': [
                'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=800&q=90',
            ],
            'tag-heuer-carrera-chronograph': [
                'https://images.unsplash.com/photo-1533139502658-0198f920d8e8?w=800&q=90',
            ],
            'cartier-santos-medium': [
                'https://images.unsplash.com/photo-1509941943102-10c232fc1571?w=800&q=90',
            ],
            'cartier-tank-francaise': [
                'https://images.unsplash.com/photo-1639037687665-8ff2d73f467a?w=800&q=90',
            ],
            'rolex-gmt-master-ii': [
                'https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=800&q=90',
            ],
            'ap-royal-oak-offshore-diver': [
                'https://images.unsplash.com/photo-1612817288484-6f916006741a?w=800&q=90',
            ],
            'patek-philippe-aquanaut-5168g': [
                'https://images.unsplash.com/photo-1606744888344-493238951221?w=800&q=90',
            ],
        }

        watches_dir = os.path.join(settings.MEDIA_ROOT, 'watches')
        os.makedirs(watches_dir, exist_ok=True)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

        for slug, urls in watch_images.items():
            try:
                watch = Watch.objects.get(slug=slug)
            except Watch.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Watch not found: {slug}'))
                continue

            for i, url in enumerate(urls):
                filename = f'{slug}.jpg'
                filepath = os.path.join(watches_dir, filename)

                self.stdout.write(f'Downloading image for {watch.name}...')
                try:
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=15) as response:
                        with open(filepath, 'wb') as f:
                            f.write(response.read())

                    # Assign to watch model
                    watch.image = f'watches/{filename}'
                    watch.save()
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {watch.name}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Failed: {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! Images assigned to watches.'))
