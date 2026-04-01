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
  
  prompt: string = '';
  selectedType: 'text' | 'image' | 'video' = 'text';
  selectedStyle: string = 'general';
  
  result: string = '';
  videoUrl: string = '';
  
  isLoading: boolean = false;
  error: string = '';
  
  // Styles disponibles pour les images IA
  imageStyles = [
    { value: 'general', label: '🎨 Général' },
    { value: 'photo', label: '📷 Photo réaliste' },
    { value: 'art', label: '🖼️ Art digital' },
    { value: 'anime', label: '🎌 Anime' },
    { value: 'cinematic', label: '🎬 Cinématique' },
    { value: 'fantasy', label: '✨ Fantasy' },
    { value: 'realistic', label: '🔍 Ultra réaliste' }
  ];
  
  // ===== CONSTRUCTEUR =====
  
  constructor(private apiService: ApiService) { }
  
  // ===== MÉTHODES =====
  
  selectType(type: 'text' | 'image' | 'video'): void {
    this.selectedType = type;
    this.clearResults();
  }
  
  clearResults(): void {
    this.result = '';
    this.videoUrl = '';
    this.error = '';
  }
  
  generate(): void {
    if (!this.prompt.trim()) {
      this.error = 'Veuillez entrer un prompt';
      return;
    }
    
    this.clearResults();
    this.isLoading = true;
    
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
  
  private generateImage(): void {
    this.apiService.generateImage(this.prompt, this.selectedStyle).subscribe({
      next: (response: GenerateResponse) => {
        this.result = response.result;
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.message || 'Erreur lors de la génération de l\'image';
        this.isLoading = false;
      }
    });
  }
  
  private generateVideo(): void {
    this.apiService.generateVideo(this.prompt).subscribe({
      next: (blob: Blob) => {
        this.videoUrl = URL.createObjectURL(blob);
        this.isLoading = false;
      },
      error: (err) => {
        this.error = err.message || 'Erreur lors de la génération de la vidéo';
        this.isLoading = false;
      }
    });
  }
  
  download(): void {
    const a = document.createElement('a');
    
    if (this.selectedType === 'text' && this.result) {
      const blob = new Blob([this.result], { type: 'text/plain' });
      a.href = URL.createObjectURL(blob);
      a.download = 'generated_text.txt';
    } else if (this.selectedType === 'image' && this.result) {
      a.href = this.result;
      a.download = 'generated_image.png';
    } else if (this.selectedType === 'video' && this.videoUrl) {
      a.href = this.videoUrl;
      a.download = 'generated_video.mp4';
    }
    
    a.click();
  }
}