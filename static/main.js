// main.js içeriği

// Gerekli fonksiyonları Firebase SDK'dan içe aktarın.
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.3.0/firebase-app.js";

// GoogleAuthProvider ve signInWithPopup'ı doğru isimlerle içe aktarın.
import { 
    getAuth, 
    GoogleAuthProvider, // BÜYÜK G ile olmalı
    signInWithPopup ,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.3.0/firebase-auth.js";


// Your web app's Firebase configuration
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
    
// Yeni bir GoogleAuthProvider örneği oluşturun.
const provider = new GoogleAuthProvider();

// HTML'den butonu alın
const googleButton = document.getElementById('google-login-btn');

// Buton varsa olay dinleyicisini ekleyin
if (googleButton) {
    googleButton.addEventListener('click', function() {

        signInWithPopup(auth, provider)
        .then((result) => {
            const user = result.user;
            
            // 1. Kullanıcıdan gerekli bilgileri alın
            const userData = {
                // Firebase'in sağladığı benzersiz Google ID
                google_uid: user.uid, 
                // Google tarafından doğrulanmış e-posta
                email: user.email, 
                // Google'dan gelen tam ad (DisplayName)
                name: user.displayName,
                // Kullanıcının profil fotoğrafı URL'si (isteğe bağlı)
                profile_picture_url: user.photoURL 
            };
            
            console.log("Alınan veriler:", userData);

            // 2. Flask sunucusuna POST isteği gönderin
            // Bu endpoint, sunucunuzda kullanıcı kaydını yapacaktır.
            return fetch('http://127.0.0.1:5000/register_google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData)
            });
        })
        .then(response => {
            if (response.ok) {
                // Sunucuya başarıyla kaydedildikten sonra dashboard'a yönlendir
                console.log("Kullanıcı verileri sunucuya başarıyla gönderildi.");
                window.location.href = "http://127.0.0.1:5000/dashboard";
            } else {
                // Sunucudan (Flask) gelen bir hata varsa
                console.error("Sunucuya veri gönderilirken hata oluştu. Status:", response.status);
                alert("Kayıt başarısız oldu. Lütfen tekrar deneyin.");
            }
        })
        .catch((error) => {
            // Hata işleme (Yetkilendirilmiş Alanlar veya ağ/pop-up hatası)
            const errorCode = error.code;
            const errorMessage = error.message;
            
            if (errorCode === 'auth/unauthorized-domain') {
                 console.error("Yetkilendirme Alanı Hatası: localhost'u kontrol edin.");
            } else {
                 console.error("Firebase Google Giriş Hatası:", errorMessage);
            }
        });
    });
} else {
    console.error("Google giriş butonu bulunamadı!");
}