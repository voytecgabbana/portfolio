from flask import Flask, render_template, abort, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'wojtek_analyst_2026'

TRANSLATIONS = {
    'pl': {
        'nav_about': 'O mnie',
        'btn_github': 'ZOBACZ STRONĘ',
        'btn_website': 'ZOBACZ STRONĘ',
        'btn_dashboard': 'ZOBACZ DASHBOARD',
        'btn_see_project': 'ZOBACZ PROJEKT',
        'btn_back': '← WRÓĆ',
        'tech_title': 'TECHNOLOGIE:',
        'lets_work': "PRACUJMY",
        'together': "RAZEM.",
        'btn_my_github': 'MÓJ GITHUB'
    },
    'en': {
        'nav_about': 'About Me',
        'btn_github': 'VIEW WEBSITE',
        'btn_website': 'VIEW WEBSITE',
        'btn_dashboard': 'VIEW DASHBOARD',
        'btn_see_project': 'VIEW PROJECT',
        'btn_back': '← BACK',
        'tech_title': 'TECHNOLOGIES:',
        'lets_work': "LET'S WORK",
        'together': "TOGETHER.",
        'btn_my_github': 'MY GITHUB'
    }
}

projects_data = [
    {
        'slug': 'statbase',
        'title': 'STATBASE',
        'image': '/static/images/project1.jpg',
        'pl': {
            'title': 'STATBASE',
            'desc': 'Centrum analizy danych statystycznych z wizualizacją w czasie rzeczywistym.',
            'full_desc': 'STATBASE to zaawansowana platforma do wizualizacji danych statystycznych, która umożliwia użytkownikom eksplorację i analizę danych w czasie rzeczywistym. Dzięki intuicyjnemu interfejsowi i  narzędziom analitycznym, STATBASE pozwala na szybkie przekształcanie surowych danych w czytelne wykresy i raporty, ułatwiając podejmowanie świadomych decyzji biznesowych. Platforma pozwala zaimportować pliki CSV, XLSX dzięki czemu jest ona wszechstronna. Aplikacja została stworzona w celu uproszczenia użytkownikom korzystania z narzędzi analitycznych i przedstawienia im rozwiązań (takich jak automatyczne czyszczenie danych jednym przyciskiem) które nie oferuje program Excel.'
        },
        'en': {
            'title': 'STATBASE',
            'desc': 'Statistical data analysis hub with real-time visualization.',
            'full_desc': 'STATBASE is an advanced data visualization platform that allows users to explore and analyze statistical data in real-time. With an intuitive interface and analytical tools, STATBASE enables quick transformation of raw data into readable charts and reports, facilitating informed business decisions. The platform allows importing CSV, XLSX files, making it versatile. The application was created to simplify users\' access to analytical tools and provide them with solutions (such as one-click automatic data cleaning) that Excel does not offer.'
        },
        'tech': ['Python', 'Streamlit', 'Plotly'],
        'gallery': ['/static/images/statbase1.jpg', '/static/images/statbase2.jpg', '/static/images/statbase3.jpg'],
        'video': '/static/vids/statbase.mp4',
        'github': 'https://statbase-webapp.streamlit.app',
    },
    {
        'slug': 'clinic-web',
        'title': 'CLINIC WEB',
        'image': '/static/images/project2.jpg',
        'pl': {
            'title': 'CLINIC WEB',
            'desc': 'System zarządzania placówką medyczną z modułem rezerwacji.',
            'full_desc': 'Kompleksowe rozwiązanie dla medycyny lub mniejszych placówek medycznych, które chcą zautomatyzować swoje procesy. System oferuje funkcje zarządzania pacjentami, rezerwacji wizyt, zarządzania personelem oraz przechowywania historii medycznej. Dzięki intuicyjnemu interfejsowi, zarówno personel medyczny, jak i pacjenci mogą łatwo korzystać z platformy, co przyczynia się do poprawy efektywności i jakości obsługi. Program został stworzony z myślą o małych przychodniach, duże systemy zarządzania klientami są drogie i wymagają długich szkoleń personelu, Clinic Web jest prostym, intuicyjnym i w pełni wystarczającym rozwiązaniem dla placówek które dopiero się rozwijają lub cyfryzują.'
        },
        'en': {
            'title': 'CLINIC WEB',
            'desc': 'Medical facility management system with booking module.',
            'full_desc': 'Comprehensive solution for medicine or smaller medical facilities looking to automate their processes. The system offers patient management, appointment booking, staff management, and medical history storage features. With an intuitive interface, both medical staff and patients can easily use the platform, contributing to improved efficiency and quality of service. The program was created with small clinics in mind; large customer management systems are expensive and require long staff training, Clinic Web is a simple, intuitive, and fully sufficient solution for facilities that are just developing or digitizing.'
        },
        'tech': ['Flask', 'SQLAlchemy', 'Bootstrap', 'JavaScript'],
        'gallery': ['/static/images/clinic1.jpg', '/static/images/clinic2.jpg', '/static/images/clinic3.jpg'],
        'video': '/static/vids/clinicweb.mp4',
        'github': 'https://clinicweb-eiwf.onrender.com'
    },
    {
        'slug': 'Dashboard', # To będzie w adresie URL, np. /project/nazwa-linku-do-projektu
        'title': 'TABLEAU DASHBOARD', # Tytuł projektu
        'image': '/static/images/project3.jpg', # Główne zdjęcie na stronie głównej
        'pl': {
            'title': 'Raport transportu i jego bezpieczeństwa na handel międzynarodowy',
            'desc': 'Analiza bezpieczeństwa transportu w handlu międzynarodowym.',
            'full_desc': 'Pełny raport analizujący bezpieczeństwo transportu w handlu międzynarodowym, zawierający dane statystyczne i rekomendacje.'
        },
        'en': {
            'title': 'Transport Report and Safety Analysis for International Trade',
            'desc': 'Analysis of transport safety in international trade.',
            'full_desc': 'Complete report analyzing transport safety in international trade, containing statistical data and recommendations.'
        },
        'tech': ['Tableau'], # Tagi technologiczne
        'gallery': ['/static/images/tableau3.jpg', '/static/images/tableau2.jpg', '/static/images/tableau1.jpg'], # Zdjęcia do galerii
        'tableau_url': 'https://public.tableau.com/views/transportibezpieczestwovshandel/Wpywtransportuijegobezpieczestwanahandelmidzynarodowy?:language=en-US&:sid=&:display_count=n&:origin=viz_share_link'
    }
]

@app.route('/')
def home():
    lang = session.get('lang', 'pl')
    return render_template('index.html', projects=projects_data, t=TRANSLATIONS[lang], lang=lang)

@app.route('/set_lang/<lang>')
def set_lang(lang):
    if lang in ['pl', 'en']:
        session['lang'] = lang
    return redirect(url_for('home'))

@app.route('/project/<slug>')
def project_details(slug):
    lang = session.get('lang', 'pl')
    project = next((p for p in projects_data if p['slug'] == slug), None)
    if not project: abort(404)
    
    # Wybieramy treść (pl lub en). Jeśli projektu nie ma w danym języku, bierzemy pl.
    p_lang_content = project.get(lang, project['pl'])
    
    return render_template('project_details.html', 
                           project=project, 
                           p_content=p_lang_content, 
                           t=TRANSLATIONS[lang], 
                           lang=lang)
@app.route('/about')
def about():
    lang = session.get('lang', 'pl')
    return render_template('about.html', t=TRANSLATIONS[lang], lang=lang)

if __name__ == '__main__':
    app.run(debug=True)