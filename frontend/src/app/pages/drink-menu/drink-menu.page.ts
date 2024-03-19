import { Component, OnInit } from '@angular/core';
import { DrinksService, Drink } from '../../services/drinks.service';
import { ModalController } from '@ionic/angular';
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

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    public drinksSvc: DrinksService
  ) {}

  ngOnInit() {
    this.drinks = this.drinksSvc.drinks;
    this.drinksSvc.getDrinks();
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
