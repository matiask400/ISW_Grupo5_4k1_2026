import { IonApp, IonRouterOutlet, IonSplitPane, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { Redirect, Route } from 'react-router-dom';

import Menu from './components/Menu';
import Actividades from './pages/Actividades';
import ComprarEntradas from './pages/ComprarEntradas';
import Inicio from './pages/Inicio';
import Mapa from './pages/Mapa';
import CompraFinalizada from './pages/CompraFinalizada';

import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

import '@fontsource/lato/400.css';
import '@fontsource/lato/700.css';

import './theme/variables.css';
import './theme/global.css';

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <IonReactRouter>
      <IonSplitPane contentId="contenido-principal" when="lg">
        <Menu />
        <IonRouterOutlet id="contenido-principal">
          <Route exact path="/inicio" component={Inicio} />
          <Route exact path="/actividades" component={Actividades} />
          <Route exact path="/entradas" component={ComprarEntradas} />
          <Route exact path="/mapa" component={Mapa} />
          <Route exact path="/compra-finalizada" component={CompraFinalizada} />
          <Route>
            <Redirect to="/inicio" />
          </Route>

        </IonRouterOutlet>
      </IonSplitPane>
    </IonReactRouter>
  </IonApp>
);

export default App;
