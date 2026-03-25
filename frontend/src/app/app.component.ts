import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService, GenerateResponse } from './services/api.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  
  // ===== VARIABLES =====
  
  prompt: string = '';                    // Le texte entré par l'utilisateur
  selectedType: 'text' | 'image' | 'video' = 'text';  // Type de génération
  
  result: string = '';                    // Résultat texte ou image base64
  videoUrl: string = '';                  // URL de la vidéo générée
  
  isLoading: boolean = false;             // État de chargement
  error: string = '';                     // Message d'erreur
  
  // ===== CONSTRUCTEUR =====
  
  constructor(private apiService: ApiService) { }
  
  // ===== MÉTHODES =====
  
  /**
   * Sélectionner le type de génération
   */
  selectType(type: 'text' | 'image' | 'video'): void {
    this.selectedType = type;
    this.clearResults();
  }
  
  /**
   * Effacer les résultats précédents
   */
  clearResults(): void {
    this.result = '';
    this.videoUrl = '';
    this.error = '';
  }
  
  /**
   * Générer le contenu
   */
  generate(): void {
    // Vérifier que le prompt n'est pas vide
    if (!this.prompt.trim()) {
      this.error = 'Veuillez entrer un prompt';
      return;
    }
    
    // Réinitialiser
    this.clearResults();
    this.isLoading = true;
    
    // Appeler la bonne méthode selon le type
    switch (this.selectedType) {
      case 'text':
        this.generateText();
        break;
      case 'image':
        this.generateImage();
        break;
      case 'video':
        this.generateVideo();
        break;
    }
  }
  
  /**
   * Générer du texte
   */
  private generateText(): void {
    this.apiService.generateText(this.prompt).subscribe({
      next: (response: GenerateResponse) => {
        this.result = response.result;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.message || 'Erreur lors de la génération du texte';
        this.isLoading = false;
      }
    });
  }
  
  /**
   * Générer une image
   */
  private generateImage(): void {
    this.apiService.generateImage(this.prompt).subscribe({
      next: (response: GenerateResponse) => {
        this.result = response.result;  // Image en base64
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.message || 'Erreur lors de la génération de l\'image';
        this.isLoading = false;
      }
    });
  }
  
  /**
   * Générer une vidéo
   */
  private generateVideo(): void {
    this.apiService.generateVideo(this.prompt).subscribe({
      next: (blob: Blob) => {
        // Créer une URL pour le blob vidéo
        this.videoUrl = URL.createObjectURL(blob);
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.message || 'Erreur lors de la génération de la vidéo';
        this.isLoading = false;
      }
    });
  }
  
  /**
   * Télécharger le résultat
   */
  download(): void {
    if (this.selectedType === 'text' && this.result) {
      // Télécharger le texte comme fichier .txt
      const blob = new Blob([this.result], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'generated_text.txt';
      a.click();
      URL.revokeObjectURL(url);
    } else if (this.selectedType === 'image' && this.result) {
      // Télécharger l'image
      const a = document.createElement('a');
      a.href = this.result;
      a.download = 'generated_image.png';
      a.click();
    } else if (this.selectedType === 'video' && this.videoUrl) {
      // Télécharger la vidéo
      const a = document.createElement('a');
      a.href = this.videoUrl;
      a.download = 'generated_video.mp4';
      a.click();
    }
  }
}