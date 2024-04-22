import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';


//todo [ ] make nicer...
@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.page.html',
  styleUrls: ['./user-page.page.scss'],
})
export class UserPagePage implements OnInit {
  loginURL: string;
  decoded: any;
  showToken: boolean = false;
  tokenButton: string = 'Show Token';

  constructor(public auth: AuthService) {
    this.loginURL = auth.build_login_link('/tabs/user-page');
    this.decoded = auth.decodeJWT(auth.token); 
    console.log(auth.decodeJWT(auth.token));
  }

  ngOnInit() {
  }

  toggleToken(){
    this.showToken = !this.showToken;
    this.tokenButton = this.showToken ? 'Hide Token' : 'Show Token';
  }

  logOut() {
    this.decoded = null;
    this.auth.logout();
  }
}
