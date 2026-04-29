import { Injectable, signal, computed } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { isDevMode } from '@angular/core';

// ======================================================
// INTERFACES
// ======================================================

export interface User {
  user_id: number;
  nom: string;
  email: string;
}

export interface RegisterRequest {
  nom: string;
  email: string;
  password: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: number;
  nom: string;
  email: string;
}

// ======================================================
// SERVICE
// ======================================================

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = isDevMode()
    ? 'http://localhost:8000'
    : 'https://projet-ia-generative.onrender.com';

  // ======================================================
  // SIGNALS (état réactif)
  // ======================================================
  // Signal = variable réactive
  // Quand elle change → Angular met à jour l'interface auto
  
  // L'utilisateur connecté (null si non connecté)
  private currentUserSignal = signal<User | null>(null);
  
  // Le token JWT
  private tokenSignal = signal<string | null>(null);

  // ======================================================
  // COMPUTED (valeurs dérivées)
  // ======================================================
  // Calculées automatiquement depuis les signals
  
  // Est-ce que l'utilisateur est connecté ?
  isAuthenticated = computed(() => this.currentUserSignal() !== null);
  
  // L'utilisateur courant (lecture seule)
  currentUser = computed(() => this.currentUserSignal());
  
  // Le token courant (lecture seule)
  token = computed(() => this.tokenSignal());

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    // Au démarrage, vérifie si un token existe dans localStorage
    // Cela permet de rester connecté après avoir fermé le navigateur
    this.loadFromStorage();
  }

  // ======================================================
  // INSCRIPTION
  // ======================================================

  register(data: RegisterRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}/auth/register`,
      data
    ).pipe(
      // tap = effectue une action sans modifier la valeur
      tap(response => this.saveSession(response))
    );
  }

  // ======================================================
  // CONNEXION
  // ======================================================

  login(data: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(
      `${this.apiUrl}/auth/login`,
      data
    ).pipe(
      tap(response => this.saveSession(response))
    );
  }

  // ======================================================
  // DÉCONNEXION
  // ======================================================

  logout(): void {
    // Supprime les données du localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // Remet les signals à null
    this.currentUserSignal.set(null);
    this.tokenSignal.set(null);
    
    // Redirige vers la page de login
    this.router.navigate(['/login']);
  }

  // ======================================================
  // MÉTHODES PRIVÉES
  // ======================================================

  private saveSession(response: AuthResponse): void {
    /**
     * Sauvegarde la session après login/register
     * 
     * 1. Extrait le token et les infos user
     * 2. Sauvegarde dans localStorage (persistance)
     * 3. Met à jour les signals (réactivité)
     */
    
    const user: User = {
      user_id: response.user_id,
      nom: response.nom,
      email: response.email
    };

    // Sauvegarde dans localStorage
    // → Données persistent si on ferme le navigateur
    localStorage.setItem('token', response.access_token);
    localStorage.setItem('user', JSON.stringify(user));

    // Met à jour les signals
    // → Interface se met à jour automatiquement
    this.tokenSignal.set(response.access_token);
    this.currentUserSignal.set(user);
  }

  private loadFromStorage(): void {
    /**
     * Au démarrage de l'app, recharge la session depuis localStorage
     * Permet de rester connecté après avoir fermé le navigateur
     */
    
    const token = localStorage.getItem('token');
    const userStr = localStorage.getItem('user');

    if (token && userStr) {
      try {
        const user = JSON.parse(userStr);
        this.tokenSignal.set(token);
        this.currentUserSignal.set(user);
      } catch {
        // Si les données sont corrompues, on nettoie
        this.logout();
      }
    }
  }

  // ======================================================
  // GETTER SIMPLE POUR LE TOKEN
  // ======================================================
  // Utilisé par l'interceptor
  
  getToken(): string | null {
    return localStorage.getItem('token');
  }
}