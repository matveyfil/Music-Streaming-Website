# get version from command arguments, default to latest
$version = $args[0]
if ($version -eq $null) {
  $version = "latest"
}

# build and push catalog image
cd Catalog
docker build -t maflus/catalog:$version .
docker push maflus/catalog:$version
cd ..
# build and push homepage image
cd Homepage
docker build -t maflus/homepage:$version .
docker push maflus/homepage:$version
cd ..
# build and push register-login image
cd Register
docker build -t maflus/register-login:$version .
docker push maflus/register-login:$version
cd ..
# build and push songs-history image
cd SongsHistory
docker build -t maflus/songs-history:$version .
docker push maflus/songs-history:$version
cd ..
# build and push upload-song image
cd UploadSong
docker build -t maflus/upload-song:$version .
docker push maflus/upload-song:$version
cd ..
# build and push gateway image
#docker build -t maflus/gateway:$version .
#docker push maflus/gateway:$version

# kubectl port-forward svc/home-page 8080:80 -n deployment-project
# curl http://localhost:8080
# curl http://localhost:8080/home
# curl -v http://192.168.49.2/login
# ping 192.168.49.2



'''
#catalog image
kubectl apply -f catalog-depl.yaml
kubectl apply -f catalog-svc.yaml
kubectl apply -f catalog-db-depl.yaml
kubectl apply -f catalog-db-svc.yaml
kubectl apply -f catalog-db-pv.yaml
kubectl apply -f catalog-db-pvc.yaml
#kubectl get svc catalog-container

#homepage image
kubectl apply -f homepage-depl.yaml
kubectl apply -f homepage-svc.yaml

#reg-log image
kubectl apply -f reg-log-depl.yaml
kubectl apply -f reg-log-svc.yaml
kubectl apply -f reg-log-db-depl.yaml
kubectl apply -f reg-log-db-svc.yaml
kubectl apply -f reg-log-db-pv.yaml
kubectl apply -f reg-log-db-pvc.yaml

#songs-history image
kubectl apply -f songs-history-depl.yaml
kubectl apply -f songs-history-svc.yaml

#upload-song image
kubectl apply -f upload-song-depl.yaml
kubectl apply -f upload-song-svc.yaml
kubectl apply -f upload-song-db-depl.yaml
kubectl apply -f upload-song-db-svc.yaml
kubectl apply -f upload-song-db-pv.yaml
kubectl apply -f upload-song-db-pvc.yaml
kubectl apply -f upload-song-pv.yaml
kubectl apply -f upload-song-pvc.yaml

#gateway image
kubectl apply -f ingress-gateway.yaml
'''