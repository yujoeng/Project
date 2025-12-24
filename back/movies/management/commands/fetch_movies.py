from django.core.management.base import BaseCommand
from django.conf import settings
import requests
from movies.models import Movie
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'TMDB API에서 인기 영화를 가져와 DB에 저장'

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=3,
            help='가져올 페이지 수 (1페이지=20편, 기본 3페이지=60편)'
        )

    def handle(self, *args, **options):
        pages = options['pages']
        total_saved = 0
        total_updated = 0
        
        TMDB_URL = "https://api.themoviedb.org/3"
        API_KEY = settings.TMDB_API_KEY
        
        self.stdout.write(self.style.SUCCESS(f"\n🎬 TMDB에서 영화 데이터 가져오기 시작...\n"))
        
        for page in range(1, pages + 1):
            self.stdout.write(f"📄 페이지 {page}/{pages} 처리 중...")
            
            url = f"{TMDB_URL}/movie/popular"
            params = {
                "api_key": API_KEY,
                "language": "ko-KR",
                "page": page,
                "region": "KR"
            }
            
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                for movie_data in data.get('results', []):
                    tmdb_id = movie_data['id']
                    
                    # 영화 상세 정보 가져오기
                    detail_url = f"{TMDB_URL}/movie/{tmdb_id}"
                    detail_params = {
                        "api_key": API_KEY,
                        "language": "ko-KR"
                    }
                    
                    try:
                        detail_response = requests.get(detail_url, params=detail_params, timeout=10)
                        
                        if detail_response.status_code == 200:
                            detail_data = detail_response.json()
                            
                            # DB에 저장/업데이트
                            movie, created = Movie.objects.update_or_create(
                                tmdb_id=tmdb_id,
                                defaults={
                                    'title': movie_data.get('title', ''),
                                    'original_title': movie_data.get('original_title', ''),
                                    'overview': movie_data.get('overview', ''),
                                    'poster_path': movie_data.get('poster_path', ''),
                                    'backdrop_path': movie_data.get('backdrop_path', ''),
                                    'release_date': self.parse_date(movie_data.get('release_date')),
                                    'runtime': detail_data.get('runtime'),
                                    'vote_average': movie_data.get('vote_average', 0),
                                    'vote_count': movie_data.get('vote_count', 0),
                                    'popularity': movie_data.get('popularity', 0),
                                    'genres': detail_data.get('genres', []),
                                    'original_language': movie_data.get('original_language', ''),
                                }
                            )
                            
                            if created:
                                total_saved += 1
                                self.stdout.write(
                                    self.style.SUCCESS(f"  ✅ {movie.title} - 새로 저장")
                                )
                            else:
                                total_updated += 1
                                self.stdout.write(
                                    self.style.WARNING(f"  ⚠️  {movie.title} - 업데이트")
                                )
                            
                            time.sleep(0.25)
                        
                    except requests.exceptions.RequestException as e:
                        self.stdout.write(
                            self.style.ERROR(f"  ❌ 영화 {tmdb_id} 상세정보 실패: {str(e)}")
                        )
                        continue
                
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ 페이지 {page} 실패: {str(e)}")
                )
                continue
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"✅ 새로 저장: {total_saved}편"))
        self.stdout.write(self.style.WARNING(f"⚠️  업데이트: {total_updated}편"))
        self.stdout.write(self.style.SUCCESS(f"📊 DB 총 영화: {Movie.objects.count()}편"))
        self.stdout.write("="*50 + "\n")
        
        if Movie.objects.count() >= 50:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n🎉 50편 이상 저장 완료! Fixture 생성:\n"
                    "python manage.py dumpdata movies.Movie --indent 2 > fixtures/movies.json\n"
                )
            )
    
    def parse_date(self, date_string):
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return None