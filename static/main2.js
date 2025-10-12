// main.js içeriği

// Gerekli fonksiyonları Firebase SDK'dan içe aktarın.
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";
import { 
    getAuth, 
    GoogleAuthProvider, 
    signInWithPopup 
} from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";


// 🔑 YOUR FIREBASE CONFIGURATION
const firebaseConfig = {
    apiKey: "AIzaSyChR0fgAC4xrgDf9FRpqjfWn6l4gQ_HQSU",
    authDomain: "nasqeprevoisly.firebaseapp.com",
    projectId: "nasqeprevoisly",
    storageBucket: "nasqeprevoisly.firebasestorage.app",
    messagingSenderId: "820508877235",
    appId: "1:820508877235:web:909023e58f364e7bfbebc6",
    measurementId: "G-NZ5VM53HM1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
auth.languageCode = 'tr'; 
    
const provider = new GoogleAuthProvider();

// HTML'den butonu alın (Giriş sayfasındaki ID'yi kullanıyoruz)
const googleButton = document.getElementById('google-login-btn');

if (googleButton) {
    googleButton.addEventListener('click', function() {

        // Pop-up ile giriş işlemini başlat
        signInWithPopup(auth, provider)
        .then((result) => {
            const user = result.user;
            
            // 1. Gerekli kullanıcı adını (username) oluştur
            // E-posta adresinin @ işaretinden önceki kısmı (ör: ahmet.yilmaz@gmail.com -> ahmet.yilmaz)
            const username = user.email.split('@')[0];
            
            // 2. Flask'a gönderilecek verileri hazırla (UID ve Kullanıcı Adı dahil)
            const userData = {
                google_uid: user.uid, 
                email: user.email, 
                name: user.displayName,
                
                
            };
            
            console.log("Sunucuya gönderilecek veriler:", userData);

            // 3. Flask'taki LOGIN rotasına POST isteği gönder
            return fetch('http://127.0.0.1:5000/login_google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
        })
        .then(response => {
            if (response.ok) {
                console.log("Oturum başarıyla açıldı.");
                // Başarılıysa Dashboard'a yönlendir
                window.location.href = "http://127.0.0.1:5000/dashboard";
            } else {
                // Sunucudan (Flask) gelen hatayı (örneğin "Kayıtlı değil") yakala
                return response.json().then(data => {
                    alert("Giriş başarısız: " + data.message);
                    console.error("Flask Giriş Hatası:", data.message);
                });
            }
        })
        .catch((error) => {
            // Firebase veya Network/CORS hatalarını yakala
            const errorCode = error.code;
            const errorMessage = error.message;
            
            if (errorCode === 'auth/popup-closed-by-user') {
                 console.log("Kullanıcı pop-up'ı kapattı.");
            } else {
                 console.error("Firebase/Network Hatası:", errorMessage);
            }
        });
    });
} else {
    console.warn("Google giriş butonu (ID: google-login-btn) bu sayfada bulunamadı.");
}