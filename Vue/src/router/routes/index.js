import appRoutes from "./app-routes";
import shopRoutes from "./shop-routes";
import wichtelRoutes from "./wichtel-routes";

const routes = [...appRoutes, ...shopRoutes, ...wichtelRoutes]

export default routes;

