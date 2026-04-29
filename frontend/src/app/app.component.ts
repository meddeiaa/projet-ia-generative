import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  template: `<router-outlet></router-outlet>`,
  // RouterOutlet = "fenêtre" où Angular affiche le composant
  // de la route active
  // /login    → affiche LoginComponent ici
  // /register → affiche RegisterComponent ici
  // /dashboard→ affiche DashboardComponent ici
})
export class AppComponent {}