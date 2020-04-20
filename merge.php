<?php
$CAF_TAG = trim($argv[1]);

$DEFAULT_XML_PATH = ".repo/manifests/default.xml";
$RELOADED_XML_PATH = ".repo/manifests/reloaded.xml";

$exceptions = [
    'android_manifest',
    'android_hardware_lineage_interfaces',
    'android_hardware_qcom_bt',
    'android_packages_apps_ReloadedOTA',
    'android_vendor_reloaded',
];

function getCAFURL($default_xml, $path){
    $url_prefix = "https://source.codeaurora.org/quic/la/";
    if(isset($default_xml->xpath('//manifest/project[@path="'.$path.'"]')[0])){
        $attr = $default_xml->xpath('//manifest/project[@path="'.$path.'"]')[0]->attributes();
        return $url_prefix . $attr['name'];
    }else if(isset($default_xml->xpath('//manifest/project[@name="'.$path.'"]')[0])){
        $attr = $default_xml->xpath('//manifest/project[@name="'.$path.'"]')[0]->attributes();
        return $url_prefix . $attr['name'];
    }
}

$default_xml = simplexml_load_string(file_get_contents($DEFAULT_XML_PATH));
$reloaded_xml = simplexml_load_string(file_get_contents($RELOADED_XML_PATH));

foreach($reloaded_xml->project as $project){
    $attributes = $project->attributes();
    $name = $attributes->name;
    if(in_array($name,$exceptions) || $attributes->remote != "reloaded")
        continue;
        
    $path = $attributes->path;
    $caf_url = getCAFURL($default_xml,$path);
    
    echo "\nMerging on $path \n\n";
    $progress = shell_exec("cd $path && git pull $caf_url $CAF_TAG");
    $unstaged = shell_exec("cd $path && git status -s");
    echo $progress . "\n\n";
    if($unstaged == ""){
        echo "Merge Success on $path \n\n";
        shell_exec("cd $path && git push git@github.com:ReloadedOS/$name.git HEAD:q");
    }else{
        echo "Merge Conflict on $path \n\n";
    }
}
