import { Component, OnInit } from '@angular/core';
import { DrinksService, Drink } from '../../services/drinks.service';
import {
  ModalController,
  ToastController
} from "@ionic/angular";
import { DrinkFormComponent } from './drink-form/drink-form.component';
import { AuthService, Permissions } from 'src/app/services/auth.service';
import { BehaviorSubject } from 'rxjs';

@Component({
  selector: "app-drink-menu",
  templateUrl: "./drink-menu.page.html",
  styleUrls: ["./drink-menu.page.scss"],
})
export class DrinkMenuPage implements OnInit {
  Object = Object;

  public drinks: BehaviorSubject<Drink[]> = new BehaviorSubject<Drink[]>([]);
  private isLoaded: boolean = false;

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    public drinksSvc: DrinksService,
    private toastController: ToastController
  ) {
   
    this.drinksSvc.drinks
    .subscribe((data) => {
      if (!this.isLoaded) {
        this.isLoaded = true;
        return;
      } else {
        this.presentToast(data.length)
      }
    });
    
  }

  ngOnInit() {
   // this.drinks.subscribe((data) => console.log(data));
   // this.drinks = this.drinksSvc.drinks;
    this.drinksSvc.getDrinks();
  }

  public handleSearchInput(event: any) {
    const query = event.target.value.toLowerCase();
    console.log(event, query);
    this.drinksSvc.getDrinks(query);
  }

  async presentToast(items: number) {
    const toast = await this.toastController.create({
      message: `${items} drinks found.`,
      duration: 3500,
      position: "bottom",
    });

    await toast.present();
  }

  public async openForm(activedrink: Drink | null) {
    if (
      !this.auth.can(Permissions.getDrinksDetail) &&
      !this.auth.can(Permissions.getDrinksDetails)
    ) {
      console.log("unauthorized");
      return;
    }

    const modal = await this.modalCtrl.create({
      component: DrinkFormComponent,
      componentProps: { drink: activedrink, isNew: !activedrink },
    });

    modal.present();
  }
}
