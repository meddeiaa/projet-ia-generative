import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  // ======================================================
  // ÉTAT DU FORMULAIRE
  // ======================================================
  
  email = '';
  password = '';
  
  // Signals pour l'état UI
  isLoading = signal(false);
  errorMessage = signal('');
  showPassword = signal(false);

  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    // Si déjà connecté → redirige vers dashboard
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
  }

  // ======================================================
  // SOUMISSION DU FORMULAIRE
  // ======================================================

  onSubmit(): void {
    // Validation basique
    if (!this.email || !this.password) {
      this.errorMessage.set('Veuillez remplir tous les champs');
      return;
    }

    this.isLoading.set(true);
    this.errorMessage.set('');

    this.authService.login({
      email: this.email,
      password: this.password
    }).subscribe({
      next: () => {
        // Connexion réussie !
        this.isLoading.set(false);
        
        // Redirige vers la page demandée ou dashboard
        const returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/dashboard';
        this.router.navigate([returnUrl]);
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(
          err.error?.detail || 'Email ou mot de passe incorrect'
        );
      }
    });
  }

  togglePassword(): void {
    this.showPassword.update(v => !v);
  }
}