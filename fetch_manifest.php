<?php
$tag = trim($argv[1]);

$myXMLData = file_get_contents("https://source.codeaurora.org/quic/la/platform/manifest/plain/default_{$tag}.xml?h={$tag}");
$xml = simplexml_load_string($myXMLData) or die("Error: Cannot create object");
foreach($xml->project as $each_project){
    $attributes = $each_project->attributes();
    if(isset($attributes['revision'])){
        unset($attributes['revision']);
    }
    if(isset($attributes['groups'])){
        $groups = clone $attributes['groups'];
       unset($attributes['groups']);
        //$each_project->addAttribute('groups', $groups);
    }
    if(isset($attributes['clone-depth'])){
        $groups = clone $attributes['clone-depth'];
        unset($attributes['clone-depth']);
        $each_project->addAttribute('clone-depth', $groups);
    }
}

$default = str_replace('"/>', '" />', $xml->asXML());
file_put_contents("$tag.xml", $default);
