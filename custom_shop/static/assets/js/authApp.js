import {initializeApp} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import {getAnalytics} from "https://www.gstatic.com/firebasejs/9.22.2/firebase-analytics.js";
import {getAuth, GoogleAuthProvider, signInWithRedirect, getRedirectResult, setPersistence, browserLocalPersistence, getIdToken, onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const firebaseConfig = {
    apiKey: "AIzaSyDoOuxxnrOFRaV8-jtsEp5DXIEKWwcPj44",
    authDomain: "pau-estore.firebaseapp.com",
    projectId: "pau-estore",
    storageBucket: "pau-estore.appspot.com",
    messagingSenderId: "949968823031",
    appId: "1:949968823031:web:1ad6c9473a5c1fd5ed69f2",
    measurementId: "G-C7R4ENZCGQ"
};

// Initialize Firebase

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
setPersistence(auth, browserLocalPersistence)
// var provider = new firebase.auth.GoogleAuthProvider();
const googleProvider = new GoogleAuthProvider();
googleProvider.addScope('https://www.googleapis.com/auth/userinfo.email');
googleProvider.addScope('https://www.googleapis.com/auth/userinfo.profile');

onAuthStateChanged(auth, async (user) => {
    if (user) {
        const token = await getIdToken(user)
        if (token) {
            axios.post('/browser-auth/', {}, {
                headers: {
                    "Authorization": `Token ${token}`,
                    "Accept": "application/json"
                    // 'Content-Type': 'application/x-www-form-urlencoded',
                },
            }).then((resp) => {
                if(resp?.data?.alreadyLoggedIn) {
                    return;
                }
                window.location.href = resp?.data?.next ?? '/shops/'
            })
        }
    }
})

getRedirectResult(auth)
  .then((result) => {
      if (!result) {
          return;
      }
      console.log(result)
  }).catch((error) => {
      if (error instanceof TypeError ) {
          console.error(error);
          return
      }
    // Handle Errors here.
    const errorCode = error.code;
    const errorMessage = error.message;
    // The email of the user's account used.
    const email = error.customData.email;
    // The AuthCredential type that was used.
    const credential = GoogleAuthProvider.credentialFromError(error);
            swal({
                title: "Login Failed !",
                text: `Login Failed - ${error.message} (${error.code})`,
                icon: "error",
                buttons: false,
                dangerMode: true,
            })
  });

const queryParams = new URLSearchParams(window.location.search)
if (queryParams?.get('from') === 'googleLogin') {
    const modalElem = document.getElementById('authLoadModal');
    if (modalElem) {
        const modalObj = new bootstrap.Modal(modalElem)
        modalObj?.show()
        setTimeout(() => {modalObj?.hide()},10000)
    }
}


export const loginWithGoogle = () => {
    signInWithRedirect(auth, googleProvider);
}

export const logoutUser = () => {
    signOut(auth).then(() => {
        window.location.href = '/app-logout/'
    })
}

const googleLoginButton = document.querySelector('#google-login-button')
if (googleLoginButton) {
    googleLoginButton.addEventListener('click', () => {
        googleLoginButton.disabled = true;
        googleLoginButton.innerHTML = 'Logging In...'
        const url = new URL(location);
        url.searchParams.set("from", "googleLogin");
        history.pushState({}, "", url);

        loginWithGoogle();

    })
}

const logoutButton = document.querySelector('#logout-button')
if (logoutButton) {
    logoutButton.addEventListener('click', () => {
        logoutUser()
    })
}

const logoutButtonDesktop = document.querySelector('#logout-button-desktop')
if (logoutButtonDesktop) {
    logoutButtonDesktop.addEventListener('click', () => {
        logoutUser()
    })
}

export const appAuth = (idToken) => {
    axios.post('/browser-auth/', {}, {
        headers: {
            "Authorization": `Token ${idToken}`,
            "Accept": "application/json"
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then((resp) => {
        if(resp?.data?.alreadyLoggedIn) {
            return;
        }
        window.location.href = resp?.data?.next ?? '/shops/'
    })
}

window.appAuth = appAuth;


